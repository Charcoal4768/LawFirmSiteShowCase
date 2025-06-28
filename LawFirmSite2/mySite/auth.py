from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user
from .models import Users

auth = Blueprint('auth',__name__)

@auth.route('/sign_in',methods=['GET','POST'])
def sign_in():
    if request.method == "POST":
        email = request.form.get("Email")
        pass1 = request.form.get("Pass1")
        pass2 = request.form.get("Pass2")
        user = Users.get_user_by_email(email=email)
        if not user:
            if len(email) < 4:
                flash("Email too short!", category="error")
            elif len(pass1) < 5:
                flash("Password too short!", category="error")
            elif pass1 != pass2:
                flash("Passwords dont match!")
            else:
                try:
                    new_user = Users.make_user(email=email,password=generate_password_hash(pass1,"scrypt"),username="Test")
                    login_user(user=new_user, remember=True)
                    flash("Succesfully Created Account!", category="success")
                    return redirect(url_for('views.home'))
                except Exception as e:
                    print(e)
                    flash(e,category="error")
        else:
            url = url_for('auth.login')
            flash(f"Account Already Exists! <a href = '{url}' style = 'border-bottom: 1px dotted blue;'>Login Instead</a>", category="error")
    return render_template('signin.html', user = current_user)

@auth.route('/login',methods = ['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("Email")
        pass1 = request.form.get("Pass1")
        user = Users.get_user_by_email(email=email)
        if user:
            if check_password_hash(user.password,pass1):
                try:
                    login_user(user)
                    flash(f"Logged in as {user.email}!", category="success")
                    return redirect(url_for("views.home"))
                except Exception as e:
                    print(e)
                    flash("An Error Occured", category="error")
            else:
                flash("Incorrect Account or Password!",category="error")
                return render_template('login.html', user = current_user)
        elif not user:
            flash("Incorrect Account or Password!", category="error")
            return render_template('login.html', user = current_user)
    else:
        return render_template('login.html', user = current_user)

@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('views.home'))
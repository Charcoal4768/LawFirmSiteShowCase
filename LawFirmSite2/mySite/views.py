import email, smtplib, ssl

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from email.utils import formataddr
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

Servermail = "emailtesting4768@gmail.com"
Lawyermail = "vkpandey1183@gmail.com"
port = 465
password = "jtna leya yhnk qhpx"
confirmation = "Hi,\n\nThank you for contacting us. We've received your message and will respond shortly.\n\n- Law Firm Name"

views = Blueprint('views',__name__)

def message(title, body, sender):
    msg = MIMEMultipart()
    msg["From"] = Servermail
    msg["To"] = Lawyermail
    msg['Reply-To'] = formataddr(( (sender.split('@'))[0], sender))
    msg["Subject"] = title
    msg.attach(MIMEText((body + " \nFrom: " + sender),"plain"))
    print(f"sending to {Lawyermail}")
    return msg.as_string()

def send_confirmation(to_email):
    msg = MIMEMultipart()

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)

    msg["Subject"] = "We've received your message"
    msg["From"] = Servermail
    msg["To"] = to_email
    msg.attach(MIMEText(confirmation,"plain"))

    try:
        server.login(Servermail,password=password)
        server.sendmail(Servermail,to_email,msg.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()
        flash("Confirmation Mail was sent succesfully.", category="success")


def sendMail(senderMail,title,bodyText):
    msg = message(title,bodyText,senderMail)

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)
    try:
        server.login(Servermail,password=password)
        server.sendmail(Servermail,Lawyermail,msg)
    except Exception as e:
        print(e)
        flash("There was an error!", category = "error")
    finally:
        server.quit()
        flash("Message was sent succesfully.", category="success")
        send_confirmation(senderMail)

@views.route("/home", methods=['GET','POST'])
def home():
    play_animation = False
    if request.method == "POST":
        logged = request.form.get("LoggedIn")
        other = request.form.get("OtherMail")
        if logged: 
            if len(logged)>2 and not other:
                senderMail = logged
            else:
                senderMail = other
        else:
            senderMail = request.form.get("Email")
        title = request.form.get("Title")
        bodyText = request.form.get("Body")
        if title and bodyText and senderMail:
            if len(title)>50:
                flash("Message title too long!", category = "error")
                play_animation = False
            if len(title)<2:
                flash("Message title too short!", category = "error")
                play_animation = False
            if len(bodyText)<15:
                flash("Please write more body text.", category = "error")
                play_animation = False
            else:
                sendMail(senderMail,title,bodyText)
                play_animation = True
                #print(senderMail)
        else:
            flash("Please properly fill in the form.", category = "error")
            play_animation = False
    return render_template('home.html',user = current_user, play_animation = play_animation)

@views.route("/")
def redirhome():
    return redirect(url_for('views.home'))
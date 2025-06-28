import os
import secrets
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DBNAME = "myDatabase.db"

def create_app():
    app = Flask(__name__)

    load_dotenv()
    if "SECRET_KEY" not in os.environ:
        with open(".env", "a") as f:
            key = secrets.token_hex(32)
            f.write(f"\nSECRET_KEY={key}\n")
        os.environ["SECRET_KEY"] = key
        
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DBNAME}"
    
    from .views import views
    from .auth import auth

    app.register_blueprint(auth)
    app.register_blueprint(views)

    from .models import Users

    LoginGuy = LoginManager()

    @LoginGuy.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
    LoginGuy.init_app(app)
    db.init_app(app)

    create_db(app)
    @app.errorhandler(404)
    def not_found(e):
        return render_template("other.html",user=current_user)
    return app

def create_db(app):
    # use with app.app_context
    if not os.path.exists('instance/'+DBNAME):
        with app.app_context():
            db.create_all()
            print("Database created!")
    else:
        print("Database already exists.")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_share import Share
from flask_caching import Cache
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Set the default value for SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

# Check if the DATABASE_URL environment variable is set
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Replace the URL scheme to use "ql://" instead of "://"
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace("://", "ql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

db = SQLAlchemy(app)
mail = Mail(app)
share = Share(app)
cache = Cache(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from . import routes
from .models import User, Url

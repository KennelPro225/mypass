from flask_login import LoginManager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
import secrets

a = secrets.token_hex()

app = Flask(__name__)
app.config['SECRET_KEY'] = '{}'.format(a)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mypass.db'
loginManager = LoginManager(app)
loginManager.login_view = 'login'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from mypass import routes
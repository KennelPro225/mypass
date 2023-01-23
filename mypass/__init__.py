from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b604217ce3ddfb8af8a9424f52165b286507ede0eace93a2c1e7e70930a85559'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mypass.db'
loginManager = LoginManager(app)
loginManager.login_view = 'login'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


from mypass import routes

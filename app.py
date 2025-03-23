from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import Config
from flask_migrate import Migrate
#from forms import LoginForm, RegistrationForm, ExpenseForm
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate=Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

#from routes import *
from routes import *

if __name__ == '__main__':
    app.run(debug=True)

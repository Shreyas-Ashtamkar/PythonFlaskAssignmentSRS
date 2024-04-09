import sqlite3
from flask_login import LoginManager

from ..models.Users import User
from . import dbutils

db = dbutils.get_db()
login_manager_ = LoginManager()
login_manager_.login_view = 'auth.login'
login_manager_.login_message_category = "warning"

def init_login_manager(app):
    login_manager_.init_app(app)

@login_manager_.user_loader
def load_user(user_id):
    return User.find_user(uid=user_id)

def register_user(fullname, username, password):
    user = User(fullname, username, password)
    db.session.add(user)
    db.session.commit()
    return user

def edit_user(id, fullname):
    user = User.find_user(id)
    user.fullname = fullname
    db.session.add(user)
    db.session.commit()
    return user

def check_login(username, password):
    user = User.find_by_username(username)
    if user.check_password(password):
        return user

def delete_user(id):
    user = User.find_user(id)
    db.session.delete(user)
    db.session.commit()
    

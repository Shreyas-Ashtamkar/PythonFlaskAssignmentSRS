from ..utils import dbutils
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = dbutils.get_db()

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    recipies = db.relationship('Recipie', backref='chef', lazy='dynamic')
    
    def __init__(self, fullname, username, password) -> None:
        self.fullname = fullname
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def find_user(uid) -> 'User':
        return User.find_by_id(uid)
    
    @staticmethod
    def find_by_id(uid) -> 'User':
        return User.query.get(uid)
    
    @staticmethod
    def find_by_username(uname) -> 'User':
        return User.query.filter_by(username=uname).first()

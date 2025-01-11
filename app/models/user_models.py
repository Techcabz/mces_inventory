from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='guest')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

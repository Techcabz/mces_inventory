import hashlib
import os
from flask_login import UserMixin
from ..extensions import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False, comment="0=Pending, 1=Approved, 2=Blocked")
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='guest')
 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   
    borrowings = db.relationship('Borrowing', back_populates='user', cascade='all, delete-orphan', passive_deletes=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
 
    @property
    def fullname(self):
        return f"{self.firstname} {self.middlename} {self.lastname}".strip()


    def __repr__(self):
        return f"<User {self.id}: {self.firstname} {self.middlename} {self.lastname} {self.status}>"


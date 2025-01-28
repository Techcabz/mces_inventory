import hashlib
import os
from flask_login import UserMixin
from ..extensions import db
from datetime import datetime

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        salt = os.urandom(16)
        hash_bytes = hashlib.scrypt(
            password.encode('utf-8'),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
        )
        self.password_hash = f"scrypt:{salt.hex()}:{hash_bytes.hex()}"

    def check_password(self, password):
        try:
            algo, salt, hash_bytes = self.password_hash.split(":")
            if algo != "scrypt":
                return False
            salt = bytes.fromhex(salt)
            stored_hash = bytes.fromhex(hash_bytes)
            computed_hash = hashlib.scrypt(
                password.encode('utf-8'),
                salt=salt,
                n=2**14,
                r=8,
                p=1,
            )
            return computed_hash == stored_hash
        except ValueError:
            return False
        
        
    def __repr__(self):
        return f"<User {self.id}: {self.firstname} {self.middlename} {self.lastname}>"


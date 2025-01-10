from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='guest')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

   # Create a new user
    def create_user(email, password, role='guest'):
        user = User(email=email, role=role)
        user.set_password(password) 

        db.session.add(user)  
        db.session.commit()
        return user
    
    # Get a user by ID
    def get_user_by_id(user_id):
        return User.query.get(user_id)  

    # Get a user by email
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    # Update user password and role
    def update_user(user_id, new_password=None, new_role=None):
        user = User.query.get(user_id) 
        if user:
            if new_password:
                user.set_password(new_password) 
            if new_role:
                user.role = new_role 
            db.session.commit()  
            return user
        return None
    
    # Delete a user by ID
    def delete_user(user_id):
        user = User.query.get(user_id)  
        if user:
            db.session.delete(user)  
            db.session.commit()  
            return True
        return False 

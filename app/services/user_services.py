# services/user_service.py
import os
from ..models.user_models import User
from ..extensions import db
from dotenv import load_dotenv

class UserService:
    @staticmethod
    def create_user(username, password, role='guest', **kwargs):
        user = User(username=username, role=role, **kwargs)
        
        user.set_password(password)
    
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def count_admins():
        return User.query.filter_by(role="admin").count()

    @staticmethod
    def update_user(user_id, new_password=None,new_username=None, new_role=None, **kwargs):
        user = User.query.get(user_id)
        if user:
            if new_password:
                user.set_password(new_password)
            if new_username:
                user.username = new_username
            if new_role:
                user.role = new_role
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            try:
                db.session.commit()
                return user
            except Exception as e:
                db.session.rollback()
                print(f"Error updating user: {e}")
        return None

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error deleting user: {e}")
        return False  
  
    @staticmethod
    def create_default_admin():
        # Load .env file
        load_dotenv()

        admin_username = "admin"
        admin_password = "admin123"
        admin_role = "admin"
       
        if os.getenv("CREATE_DEFAULT_ADMIN", "true").lower() == "true":
  
            existing_admin = UserService.get_user_by_username(username=admin_username)
            if not existing_admin:
                default_data = {
                    "firstname": "admin",
                    "lastname": "admin",
                    "email": "admin@gmail.com",
                    "middlename": "",
                    "sex": "male",
                    "status": 1,
                    "address": "admin address",
                    "contact": "0000000000",
                }
                admin = UserService.create_user(
                    username=admin_username,
                    password=admin_password,
                    role=admin_role,
                    **default_data,
                )
                if admin:
                    print(f"Default admin user created with username: {admin_username} & {admin_password}")
                else:
                    print("Failed to create default admin user.")
            else:
                print("Default admin user already exists.")

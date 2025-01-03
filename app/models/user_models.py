# app/models.py

from flask_login import UserMixin

# Example in-memory user store
users = {
    'admin': {'password': 'adminpass', 'role': 'admin'},
    'guest': {'password': 'guestpass', 'role': 'guest'}
}

class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def get_id(self):
        return self.id

    def is_admin(self):
        return self.role == 'admin'

    @classmethod
    def get(cls, user_id):
        user_data = users.get(user_id)
        if user_data:
            return User(user_id, user_data['role'])
        return None

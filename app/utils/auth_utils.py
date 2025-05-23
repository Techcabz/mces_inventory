from flask import redirect, url_for, session, flash
from flask_login import current_user
from functools import wraps

def web_guard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('main.login')) 

        if session.get('role') != 'admin': 
            flash('Access denied: Admins only!', 'error')
            return redirect(url_for('main.user_dashboard')) 
        return func(*args, **kwargs)
    return wrapper


def web_guard_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('main.login')) 

        if session.get('role') != 'guest': 
            return redirect(url_for('main.user_dashboard')) 
        return func(*args, **kwargs)
    return wrapper


def web_auth_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return func(*args, **kwargs)
  
        if session.get('role') == 'guest':
            return redirect(url_for('main.user_dashboard'))
        else:
            return redirect(url_for('admin.dashboard'))
    return wrapper
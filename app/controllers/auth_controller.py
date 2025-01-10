from flask import flash, redirect, url_for, request
from flask_login import login_user,logout_user
from flask import session
from app.models.user_models import User
from ..extensions import db

def login_user_controller(request):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.get_user_by_email(email)
        
        if user and user.check_password(password):
            login_user(user)
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard')) 
        else:
            flash('Invalid email or password.', 'danger')

    return None

def register_user_controller(request):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not email or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return None

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return None

        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'danger')
            return None

        new_user = User(email=email, role='guest')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return None

def logout_user_controller():
    logout_user()
    session.clear() 
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))
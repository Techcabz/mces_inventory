# app/views/admin.py

from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_login import current_user
from functools import wraps


admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if the user is logged in
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('main.login')) 

        # Check if the user has the 'admin' role
        if session.get('role') != 'admin': 
            flash('Access denied: Admins only!', 'error')
            return redirect(url_for('main.home')) 
        return func(*args, **kwargs)
    return wrapper


@admin.route('/dashboard')
@admin_required
def dashboard():
    print(session)
    return render_template('admin/dashboard.html')

@admin.route('/category')
# @admin_required
def category():
    print(session)
    return render_template('admin/category.html')

@admin.route('/borrowing')
# @admin_required
def borrowing():
    print(session)
    return render_template('admin/borrowing.html')


@admin.route('/materials')
# @admin_required
def materials():
    print(session)
    return render_template('admin/materials.html')

@admin.route('/equipment')
# @admin_required
def equipment():
    print(session)
    return render_template('admin/equipment.html')

@admin.route('/tools')
# @admin_required
def tools():
    print(session)
    return render_template('admin/tools.html')


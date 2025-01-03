# app/views/admin.py

from flask import Blueprint, render_template, redirect, url_for, session, flash

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Access denied: Admins only!', 'error')
            return redirect(url_for('main.home'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin.route('/dashboard')
# @admin_required
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
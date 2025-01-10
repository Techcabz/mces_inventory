from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from ..controllers.auth_controller import login_user_controller,logout_user_controller,register_user_controller
from ..utils.auth_utils import admin_required
from ..models.user_models import User
from ..extensions import db

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')

# AUTHENTICATION
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    result = login_user_controller(request)
    if result:
        return result
    return render_template('auth/login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    return render_template('auth/register.html')

@main.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    result = register_user_controller(request)
    if result:
        return result
    return render_template('auth/login.html')

@main.route('/logout')
def logout():
    return logout_user_controller()



# ADMINISTRATOR
@admin.route('/dashboard')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/category')
@admin_required
def category():
    return render_template('admin/category.html')

@admin.route('/borrowing')
@admin_required
def borrowing():
    return render_template('admin/borrowing.html')

@admin.route('/materials')
@admin_required
def materials():
    return render_template('admin/materials.html')

@admin.route('/equipment')
@admin_required
def equipment():
    return render_template('admin/equipment.html')

@admin.route('/tools')
@admin_required
def tools():
    return render_template('admin/tools.html')

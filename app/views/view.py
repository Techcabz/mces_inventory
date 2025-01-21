from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import  current_user
from ..controllers.auth_controller import login_user_controller,logout_user_controller,register_user_controller
from ..utils.auth_utils import web_guard
from ..models.user_models import User
from ..extensions import db

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')

# AUTHENTICATION
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))
    return login_user_controller(request)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))
    return register_user_controller(request)

@main.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated and request.endpoint != 'admin.dashboard':
        return redirect(url_for('admin.dashboard'))
    return login_user_controller(request)

@main.route('/logout')
def logout():
    return logout_user_controller()


# ADMINISTRATOR
@admin.route('/dashboard')
@web_guard
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/category')
@web_guard
def category():
    return render_template('admin/category.html')

@admin.route('/borrowing')
@web_guard
def borrowing():
    return render_template('admin/borrowing.html')

@admin.route('/materials')
@web_guard
def materials():
    return render_template('admin/materials.html')

@admin.route('/equipment')
@web_guard
def equipment():
    return render_template('admin/equipment.html')

@admin.route('/tools')
@web_guard
def tools():
    return render_template('admin/tools.html')
@admin.route('/logs')
@web_guard
def logs():
    return render_template('admin/logs.html')


@main.route('/test')
def test():
    return render_template('auth/test.html')

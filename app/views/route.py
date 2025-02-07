from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import  current_user
from app.controllers.auth_controller import login_user_controller,logout_user_controller,register_user_controller
from app.controllers.categories_controller import categories
from app.controllers.inventory_controller import inventories
from app.utils.auth_utils import web_guard
from app.models.user_models import User
from app.extensions import db

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')

# AUTHENTICATION
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    return login_user_controller(request)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    return register_user_controller(request)

@main.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    return login_user_controller(request)

@main.route('/logout', methods=['GET', 'POST'])
def logout():
    return logout_user_controller()


# ADMINISTRATOR
@admin.route('/dashboard')
@web_guard
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/borrowing')
@web_guard
def borrowing():
    return render_template('admin/borrowing.html')

@admin.route('/category', methods=['GET', 'POST', 'PUT', 'DELETE'])
@web_guard
def category():
    return categories(request)

@admin.route('/inventory', methods=['GET', 'POST'])
@admin.route('/inventory/<int:inventory_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def inventory(inventory_id=None):
    return inventories(request, inventory_id)


@admin.route('/reports')
@web_guard
def reports():
    return render_template('admin/logs.html')

@admin.route('/settings')
@web_guard
def settings():
    return render_template('admin/logs.html')

@admin.route('/logs')
@web_guard
def logs():
    return render_template('admin/logs.html')

@admin.route('/users')
@web_guard
def users():
    return render_template('admin/users.html')


@main.route('/test')
def test():
    return render_template('auth/test.html')

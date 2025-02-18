from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import  current_user
from app.controllers.auth_controller import login_user_controller,logout_user_controller,register_user_controller
from app.controllers.categories_controller import categories
from app.controllers.inventory_controller import inventories
from app.controllers.users_controller import cusers,user_approved,user_disapproved
from app.controllers.item_controller import items, search_items
from app.controllers.borrowing_controller import borrowings, borrowings_status,borrowings_cancel_reason,borrowings_done
from app.utils.auth_utils import web_guard,web_guard_user
from app.models.user_models import User
from app.extensions import db
from uuid import UUID

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')
# user = Blueprint('admin', __name__, url_prefix='/user')

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

@admin.route('/borrowing', methods=['GET', 'POST'])
# @main.route('/borrowing/item/<uuid:item_uuid>', methods=['POST','GET', 'PUT', 'DELETE'])
@web_guard
def borrowing(item_uuid=None):
    return borrowings(request,item_uuid)

@admin.route("/borrowing/status/<int:borrowing_id>", methods=['GET', 'POST', 'PUT',])
@web_guard
def borrowing_status(borrowing_id=None):
    return borrowings_status(request, borrowing_id)

@admin.route("/borrowing/done/<int:borrowing_id>", methods=['GET', 'POST', 'PUT',])
@web_guard
def borrowing_done(borrowing_id=None):
    return borrowings_done(request, borrowing_id)

@admin.route("/borrowing/cancel_reason/<int:borrowing_id>", methods=['GET', 'POST', 'PUT',])
@web_guard
def borrowing_cancel_reason(borrowing_id=None):
    return borrowings_cancel_reason(request, borrowing_id)

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

@admin.route('/users', methods=['GET'])
@admin.route('/users/<int:users_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def users(users_id=None):
    return cusers(request,users_id)

@admin.route('/users/approved/<int:users_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def users_approved(users_id=None):
    return user_approved(request,users_id)

@admin.route('/users/disapproved/<int:users_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def user_disapproveds(users_id=None):
    return user_disapproved(request,users_id)


@main.route('/test')
def test():
    return render_template('auth/test.html')

# USER DASHBOARD
@main.route('/user/dashboard')
@main.route('/users/item/<uuid:item_uuid>', methods=['POST','GET', 'PUT', 'DELETE'])
@web_guard_user
def user_dashboard(item_uuid=None):
    return items(request,item_uuid)


@main.route('/search-items')
@web_guard_user
def search_item():
    return search_items()
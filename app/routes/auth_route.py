from . import main, redirect,url_for,request
from flask_login import  current_user
from app.controllers.auth_controller import login_user_controller,logout_user_controller,register_user_controller
from app.controllers.users_controller import home_user_controller
from app.utils.auth_utils import web_auth_user


@main.route('/', methods=['GET', 'POST'])
@web_auth_user
def home():
    return home_user_controller(request)


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

@main.route('/logout', methods=['GET', 'POST'])
def logout():
    return logout_user_controller()

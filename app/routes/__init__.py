from flask import Blueprint
from app.utils.auth_utils import web_guard,web_guard_user
from flask import  render_template, redirect, url_for, request


# Define Blueprints
main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__, url_prefix='/admin')
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Import route modules to register routes
from app.routes.auth_route import * 
from app.routes.admin_route import *
from app.routes.user_routes import *

# Store Blueprints in a list for easy registration
all_blueprints = [auth,admin, main]  

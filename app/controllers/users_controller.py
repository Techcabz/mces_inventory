from flask import  request,render_template
from flask import jsonify
from app.services.services import CRUDService
from app.models.user_models import User
from flask_login import login_required, current_user
from app.utils.validation_utils import Validation
from app.services.user_services import UserService
from app.models.borrowing_models import Borrowing

user_services = CRUDService(User)
borrow_services= CRUDService(Borrowing)


def cusers(request,users_id=None):
    if request.method == 'GET':
        users = user_services.get()
        pending_count = sum(1 for user in users if user.status == 0)

        return render_template('admin/users.html', users=users, pendingCount=pending_count)
    return jsonify({'success': False, 'message': 'Create method must be POST.'}), 405

def user_approved(request,users_id=None):
    if request.method == 'PUT':
        users = user_services.get_one(id=users_id)
        if not users:
            return jsonify({'success': False, 'message': 'Invalid User'}), 405
        
        data = request.json
        new_status = int(data.get("status"))
        
        user_services.update(users_id,status=new_status)
        return jsonify({'success': False, 'message': 'User approved successfully.'}), 200
    
    return jsonify({'success': False, 'message': 'Create method must be POST.'}), 405


def user_disapproved(request,users_id=None):
    if request.method == 'DELETE':
        users = user_services.get_one(id=users_id)
        if not users:
            return jsonify({'success': False, 'message': 'Invalid User'}), 404
    
        user_services.delete(id=users_id)
        return jsonify({'success': False, 'message': 'User remove successfully.'}), 200
    
    return jsonify({'success': False, 'message': 'Create method must be DELETE.'}), 405


def get_profiles_admin(users_id):
    user = user_services.get_one(id=users_id)
    print(user)

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "middlename": user.middlename,
        "sex": user.sex,
        "status": user.status,
        "address": user.address,
        "contact": user.contact,
        "role": user.role,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return jsonify({"success": True, "user": user_data})

def update_profile_user():
    data = request.json
    user_id = data.get("profile_user_id")
    user = user_services.get_one(id=user_id)
 
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Fields to update
    update_data = {
        "firstname": data.get("afname"),
        "middlename": data.get("amname"),
        "lastname": data.get("alname"),
        "contact": data.get("acontact"),
        "address": data.get("aaddress"),
        "sex": data.get("asex"),
    }
    new_password = data.get("newPassword")
    print(update_data)
    if new_password:  
        password_error = Validation.is_valid_password(new_password)
        if password_error:
            return jsonify({"success": False, "message": password_error}), 400

        user.set_password(new_password) 
    updated_user = user_services.update(user_id, **update_data)

    if updated_user:
        return jsonify({"success": True, "message": "Profile updated successfully"})
    else:
        return jsonify({"success": False, "message": "Error updating profile"}), 500
    
def add_admin_profile():
    data = request.json
    
    # Ensure the username is correctly retrieved from the request
    admin_username = data.get("auusername")
    admin_password = data.get("aunewPassword")
    admin_role = "admin"

    if not admin_username or not admin_password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400

    # Check if admin user already exists
    existing_admin = UserService.get_user_by_username(username=admin_username)
    if existing_admin:
        return jsonify({"success": False, "message": "Admin username already exists"}), 400

    # Count existing admin users
    admin_count = UserService.count_admins()
    if admin_count >= 5:
        return jsonify({"success": False, "message": "Maximum of 5 admins allowed"}), 400

    # Default admin data
    default_data = {
        "firstname": "admin",
        "lastname": "admin",
        "middlename": "",
        "sex": "Male",
        "status": 1,
        "address": "",
        "contact": "",
    }

    # Create admin user
    new_admin = UserService.create_user(
        username=admin_username,
        password=admin_password,
        role=admin_role,
        **default_data
    )

    if new_admin:
        return jsonify({"success": True, "message": "Admin profile created successfully"}), 201
    else:
        return jsonify({"success": False, "message": "Failed to create admin profile"}), 500


    
def update_admin_profile():
    data = request.json
    
    # Ensure the username is correctly retrieved from the request
    admin_id = data.get("profile_user_id")
    admin_username = data.get("auesername")
    new_password = data.get("aeunewPassword")
    
    print(data)
   
    if new_password:  
        new_admin = UserService.update_user(
            user_id=admin_id,
            password=new_password
        )

    # Create admin user
    new_admin = UserService.update_user(
        user_id=admin_id,
        username=admin_username
    )

    if new_admin:
        return jsonify({"success": True, "message": "Admin profile updated successfully"}), 201
    else:
        return jsonify({"success": False, "message": "Failed to updated admin profile"}), 500



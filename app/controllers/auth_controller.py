from flask import flash, redirect, url_for, request,render_template
from flask_login import login_user,logout_user
from flask import session
from app.services.user_services import UserService
from app.utils.validation_utils import Validation
from app.models.logs_models import Logs
from app.services.services import CRUDService
from flask import jsonify

log_service = CRUDService(Logs)

def login_user_controller(request):
    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserService.get_user_by_username(username)
       
        if not user:
            log_service.create(name="Login Attempt", level="WARNING", message=f"Failed login attempt for username: {username}")
            return jsonify({'error': False, 'message': 'Invalid username or password.'}), 400
        
    
        if user.status == 0:
            log_service.create(name="Login Denied", level="WARNING", message=f"Blocked login attempt for unapproved user: {username}", user_id=user.id)
            
            return jsonify({'error': False, 'message': 'Your account is pending approval. Please wait for administrator approval.'}), 403

        if user.status == 2: 
            log_service.create(name="Login Denied", level="ERROR", message=f"Blocked login attempt for user: {username} (Account blocked)", user_id=user.id)
           
            return jsonify({'error': False, 'message': 'Your account has been blocked. Please contact the administrator.'}), 403

        if user and user.check_password(password):
            login_user(user)
            session['role'] = user.role
            session['user_id'] = user.id
            session['status'] = user.status
            session['firstname'] = user.firstname 
            session['lastname'] = user.lastname
            session['fullname'] = user.fullname
            session['username'] = user.username.title() 
            log_service.create(name="Login Success", level="INFO", message=f"User {username} logged in", user_id=user.id)

            return jsonify({'success': True, 'message': 'Login successful! Redirecting...'}), 200

        log_service.create(name="Login Attempt", level="WARNING", message=f"Invalid login attempt for username: {username}", user_id=user.id if user else None)     
        return jsonify({'success': True, 'message': 'Invalid username or password.'}), 400

    return jsonify({'success': False, 'message': 'Login method must be POST.'}), 405

def register_user_controller(request):
    if request.method == 'GET':
        return render_template('auth/register.html')

    elif request.method == 'POST':
        username = request.form.get('username', '').lower()
        firstname = request.form.get('firstname', '').lower()
        lastname = request.form.get('lastname', '').lower()
        middlename = request.form.get('middlename', '').lower()  # Optional
        sex = request.form.get('sex', '').lower()
        address = request.form.get('address', '').lower()
        contact = request.form.get('contact')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate fields
        if not all([username, firstname, lastname, sex, address, contact, password, confirm_password]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        if username == "admin":
            return jsonify({'success': False, 'message': 'The username "admin" is reserved and cannot be used.'}), 400

        if not Validation.is_valid_name(firstname):
            return jsonify({'success': False, 'message': 'First name must contain only letters.'}), 400
        if Validation.has_repeated_characters(firstname):
            return jsonify({'success': False, 'message': 'First name must not have three or more consecutive repeated characters.'}), 400

        if not Validation.is_valid_name(lastname):
            return jsonify({'success': False, 'message': 'Last name must contain only letters.'}), 400
        if Validation.has_repeated_characters(lastname):
            return jsonify({'success': False, 'message': 'Last name must not have three or more consecutive repeated characters.'}), 400
        
        if len(password) < 8:
            return jsonify({'success': False, 'message': 'Password must be at least 8 characters long.'}), 400
        if not any(char.isdigit() for char in password):
            return jsonify({'success': False, 'message': 'Password must contain at least one number.'}), 400
        if not any(char.isupper() for char in password):
            return jsonify({'success': False, 'message': 'Password must contain at least one uppercase letter.'}), 400
        if not any(char in "!@#$%^&*()-_=+{}[]|;:'\",.<>?/`~" for char in password):
            return jsonify({'success': False, 'message': 'Password must contain at least one special character.'}), 400

        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match.'}), 400

        if UserService.get_user_by_username(username):
            return jsonify({'success': False, 'message': 'Username is already taken.'}), 400

        # Create new user
        new_user = UserService.create_user(
            username=username,
            password=password,
            role='guest',
            firstname=firstname,
            lastname=lastname,
            middlename=middlename,
            sex=sex,
            address=address,
            contact=contact
        )

        if new_user:
            log_service.create(name="User Registration", level="INFO", message=f"New user registered: {username}", user_id=new_user.id)
            return jsonify({'success': True, 'message': 'Registration successful! Please log in.'}), 200
        else:
            log_service.create(name="User Registration Failed", level="ERROR", message=f"Failed registration attempt for username: {username}")   
            return jsonify({'success': False, 'message': 'Failed to register. Please try again.'}), 500

    return jsonify({'success': False, 'message': 'Invalid request method.'}), 405

def logout_user_controller():
    if request.method == 'POST':
        user_id = session.get('user_id')
        username = session.get('username', 'Unknown User')

        logout_user()
        session.clear() 
        log_service.create(name="User Logout", level="INFO", message=f"User {username} logged out", user_id=user_id)

        return jsonify({'success': True, 'message': 'You have been logged out'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid request method.'}), 405
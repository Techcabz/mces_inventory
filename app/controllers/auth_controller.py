from flask import flash, redirect, url_for, request,render_template
from flask_login import login_user,logout_user
from flask import session
from app.services.user_services import UserService
from app.utils.validation_utils import Validation
from flask import jsonify

def login_user_controller(request):
    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserService.get_user_by_username(username)
       
        if not user:
            return jsonify({'error': False, 'message': 'Invalid username or password.'}), 400
        
    
        if user.status == 0:
            return jsonify({'error': False, 'message': 'Your account is pending approval. Please wait for administrator approval.'}), 403

        if user.status == 2: 
            return jsonify({'error': False, 'message': 'Your account has been blocked. Please contact the administrator.'}), 403

        if user and user.check_password(password):
            login_user(user)
            session['role'] = user.role
            session['user_id'] = user.id
            session['status'] = user.status
            session['firstname'] = user.firstname 
            session['lastname'] = user.lastname
            session['username'] = user.username.title() 
            return jsonify({'success': True, 'message': 'Login successful! Redirecting...'}), 200

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
            return jsonify({'success': True, 'message': 'Registration successful! Please log in.'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to register. Please try again.'}), 500

    return jsonify({'success': False, 'message': 'Invalid request method.'}), 405

def logout_user_controller():
    if request.method == 'POST':
        logout_user()
        session.clear() 
        return jsonify({'success': True, 'message': 'You have been logged out'}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid request method.'}), 405
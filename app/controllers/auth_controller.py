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
        
        if user and user.check_password(password):
            login_user(user)
            session['role'] = user.role
            return jsonify({'success': True, 'message': 'Login successful! Redirecting...'}), 200

        else:
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 400
    return jsonify({'success': False, 'message': 'Login method must be POST.'}), 405

def register_user_controller(request):
    if request.method == 'GET':
        return render_template('auth/register.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        middlename = request.form.get('middlename', '')  # Optional
        sex = request.form.get('sex')
        address = request.form.get('address')
        contact = request.form.get('contact')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate fields
        if not all([username, firstname, lastname, sex, address, contact, password, confirm_password]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        if not Validation.is_valid_name(firstname):
            return jsonify({'success': False, 'message': 'First name must contain only letters.'}), 400
        if not Validation.has_no_repeated_characters(firstname):
            return jsonify({'success': False, 'message': 'First name must not have three or more consecutive repeated characters.'}), 400

        if not Validation.is_valid_name(lastname):
            return jsonify({'success': False, 'message': 'Last name must contain only letters.'}), 400
        if not Validation.has_no_repeated_characters(lastname):
            return jsonify({'success': False, 'message': 'Last name must not have three or more consecutive repeated characters.'}), 400
        
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
    logout_user()
    session.clear() 
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))
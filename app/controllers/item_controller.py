from flask import request, render_template, jsonify
from app.models.inventory_models import Inventory
from app.models.category_models import Category
from app.models.borrowing_models import Borrowing
from app.models.user_models import User
from app.models.cart_models import Cart
from app.services.services import CRUDService
from app.utils.file_utils import get_inventory_image
from uuid import UUID 
from datetime import datetime
from sqlalchemy.orm import joinedload
from flask_login import login_required, current_user

from app.models.borrowing_details_model import BorrowingDetails

inventory_service = CRUDService(Inventory)
borrowing_service = CRUDService(Borrowing)
category_service = CRUDService(Category)
cancel_service = CRUDService(BorrowingDetails)
cart_service = CRUDService(Cart)
user_services = CRUDService(User)


def items(request, inventory_uuid=None):  
    
    if request.method == 'GET':
       
        if inventory_uuid:
            try:
                uuid_obj = UUID(str(inventory_uuid)) 
               
                inventory = inventory_service.get_one(uuid=str(uuid_obj)) 
               
            except ValueError:
                return render_template('404.html'), 404

            if not inventory:
                return render_template('404.html'), 404

            inventory_data = inventory.serialize()
            inventory_data['image_url'] = get_inventory_image(inventory.image)
            inventory_data['uuid'] = inventory.uuid
            
            return render_template('user/single_item.html', inventory=inventory_data)

        item_list = inventory_service.get()
        categories = category_service.get()
        
        category_items = {category.name.lower(): [] for category in categories}

        for item in item_list:
            item.image_url = get_inventory_image(item.image)
            category_name = item.category.name.lower()
            
            if category_name in category_items:
                category_items[category_name].append(item)
            else:
                category_items[category_name] = [item]

            
        return render_template('user/dashboard.html',  categories=categories, category_items=category_items)


def borrow_items(request):
    if request.method == 'POST':
        user_id = request.form['user_id'].strip().lower()
        start_date_str = request.form['start_date'].strip().lower()
        end_date_str = request.form['end_date'].strip().lower()

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            today = datetime.today().date()

            if start_date < today:
                return jsonify({'success': False, 'message': 'Start date cannot be in the past.'}), 400
                
            if end_date <= start_date:
                return jsonify({'success': False, 'message': 'End date must be after the start date.'}), 400

        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

        cart_items = [item for item in cart_service.get(user_id=user_id) if item.status == "pending"]

        if not cart_items:
            return jsonify({'success': False, 'message': "No pending items in your cart!"}), 400

        # Check availability before proceeding
        for cart_item in cart_items:
            inventory = inventory_service.get_one(id=cart_item.inventory_id)
            if not inventory or inventory.quantity < cart_item.quantity:
                return jsonify({
                    'success': False,
                    'message': f"⚠️ Not enough stock for {inventory.title}. Available: {inventory.quantity}, Requested: {cart_item.quantity}."
                }), 400

        # Create borrowing without modifying inventory yet
        borrowing = borrowing_service.create(user_id=user_id, start_date=start_date, end_date=end_date)

        if not borrowing:
            return jsonify({'success': False, 'message': 'Failed to create borrowing request.'}), 500

        for cart_item in cart_items:
            borrowing_service.add_to_relationship(borrowing.id, 'cart_items', cart_item)
            cart_service.update(cart_item.id, status="completed")

        return jsonify({
            'success': True,
            'message': 'Your borrowing request has been submitted and is pending approval from the admin.'
        }), 200

    return jsonify({'success': False, 'message': 'Create method must be POST.'}), 405


def users_borrowed(request, borrow_uuid=None):
    now = datetime.utcnow()

    if not borrow_uuid:
        borrowing_list = Borrowing.query.options(joinedload(Borrowing.cart_items)).all()

        for borrowing in borrowing_list:
            borrowing.days_remaining, borrowing.days_late = calculate_borrowing_days(borrowing, now)
            borrowing.inventory_titles = format_inventory_titles(borrowing)

        return render_template('user/borrowed.html', borrowings=borrowing_list)

    # 🔹 Fetch single borrowing record if UUID is provided
    try:
        uuid_obj = UUID(str(borrow_uuid))
        borrowing_single = Borrowing.query.options(
            joinedload(Borrowing.cart_items),  
            joinedload(Borrowing.details)  
        ).filter_by(uuid=str(uuid_obj)).first()

        if not borrowing_single:
            return render_template('404.html'), 404

        borrowing_single.start_date_str = borrowing_single.start_date.strftime("%B %d, %Y") if borrowing_single.start_date else "N/A"
        borrowing_single.end_date_str = borrowing_single.end_date.strftime("%B %d, %Y") if borrowing_single.end_date else "N/A"

        borrowing_single.days_remaining, borrowing_single.days_late = calculate_borrowing_days(borrowing_single, now)
        borrowing_single.inventory_titles = format_inventory_titles(borrowing_single)
        print("Borrowing Object Data:", borrowing_single.__dict__)  # Debugging

        return render_template('user/borrowed_single.html', borrowing=borrowing_single)

    except ValueError:
        return render_template('404.html'), 404

def calculate_borrowing_days(borrowing, now):
    if borrowing.end_date:
        days_remaining = (borrowing.end_date.date() - now.date()).days
        
        if days_remaining >= 0:
            return days_remaining, 0  # Not overdue yet
        else:
            return 0, abs(days_remaining)  # Convert to positive overdue days
    
    return None, None




# 🔹 Helper function to format inventory titles
def format_inventory_titles(borrowing):
    if borrowing.cart_items:
        return [
            f"{cart_item.inventory_item.title.capitalize()} (Qty: {cart_item.quantity})"
            for cart_item in borrowing.cart_items if cart_item.inventory_item
        ]
    return []

def search_items():
    query = request.args.get("q", "").strip().lower() 
    print(query)
    if not query:
        # If no query, return all items grouped by category
        items = inventory_service.get()
        return jsonify([
            {
                "title": item.title.capitalize(),
                "image_url": get_inventory_image(item.image),
                "quantity": item.quantity,
                "uuid": item.uuid,
                "status": item.status.capitalize(),
                "category": item.category.name.capitalize() if item.category else "Uncategorized",
            }
            for item in items
        ])

    # If query exists, filter items
    items = inventory_service.get()
    filtered_items = [
        {
            "title": item.title.capitalize(),
            "image_url": get_inventory_image(item.image),
            "quantity": item.quantity,
             "uuid": item.uuid,
            "status": item.status.capitalize(),
            "category": item.category.name.capitalize() if item.category else "Uncategorized",
        }
        for item in items if query in item.title.lower() or query in (item.category.name.lower() if item.category else "")
    ]

    return jsonify(filtered_items)

def borrowing_status_user(request, borrowing_id=None):
    if request.method == 'PUT':
        borrowing = borrowing_service.get_one(id=borrowing_id)

        if not borrowing:
            return jsonify({'success': False, 'message': 'Borrowing record not found'}), 404
        
        data = request.json
        new_status = data.get("status")
        
        for cart_item in borrowing.cart_items:
            inventory = inventory_service.get_one(id=cart_item.inventory_id)  

            if not inventory:
                return jsonify({'success': False, 'message': f'Inventory ID {cart_item.inventory_id} not found'}), 404

            inventory.quantity += cart_item.quantity

            if inventory.quantity > 0:
                inventory.status = 'available'

            inventory_service.update(inventory)


        borrowing_service.update(borrowing.id, status=new_status)
        return jsonify({'success': True, 'message': 'Cancellation request approved'}), 200
    return jsonify({'error': False, 'message': 'Invalid Method'}), 400

def get_profiles(request):
    if request.method == 'GET':
        if current_user.is_authenticated:
            user_data = {
                "id": current_user.id,
                "username": current_user.username,
                "firstname": current_user.firstname,
                "lastname": current_user.lastname,
                "middlename": current_user.middlename,
                "sex": current_user.sex,
                "status": current_user.status,
                "address": current_user.address,
                "email": current_user.email,
                "contact": current_user.contact,
                "role": current_user.role,
                "created_at": current_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": current_user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }

        return jsonify({"success": True, "user": user_data})
    return jsonify({'success': False, 'message': 'Create method must be GET.'}), 405


def update_profiles():
    data = request.json
    user_id = current_user.id
    user = user_services.get_one(id=user_id)

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Fields to update
    update_data = {
        "firstname": data.get("fname"),
        "middlename": data.get("mname"),
        "lastname": data.get("lname"),
        "contact": data.get("contact"),
         "email": data.get("email"),
        "address": data.get("address"),
        "sex": data.get("sex"),
    }

    # Handle password update
    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    if new_password:  # User wants to change password
        if not current_password:
            return jsonify({"success": False, "message": "Current password is required to change password"}), 400
        
        if not user.check_password(current_password):  # Use model method
            return jsonify({"success": False, "message": "Incorrect current password"}), 400

         # Validate new password
        password_error = is_valid_password(new_password)
        if password_error:
            return jsonify({"success": False, "message": password_error}), 400

        user.set_password(new_password)  # Use model method

    # Update user information
    updated_user = user_services.update(user_id, **update_data)

    if updated_user:
        return jsonify({"success": True, "message": "Profile updated successfully"})
    else:
        return jsonify({"success": False, "message": "Error updating profile"}), 500
    
def is_valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char in "!@#$%^&*()-_=+{}[]|;:'\",.<>?/`~" for char in password):
        return "Password must contain at least one special character."
    return None  # Password is valid
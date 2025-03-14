from app.models.cart_models import Cart
from app.models.inventory_models import Inventory
from app.services.services import CRUDService
from flask import request, render_template, jsonify, url_for
from uuid import UUID
from flask_login import current_user, login_required 

inventory_service = CRUDService(Inventory)
cart_service = CRUDService(Cart)


def view_cart():
    cart_items = [item for item in cart_service.get(user_id=current_user.id) if item.status == "pending"]
    
    return render_template('user/cart.html', cart_list=cart_items)


def get_cart_count():
    if not current_user.is_authenticated:
        return jsonify({'count': 0})  
    
    cart_items = cart_service.get(user_id=current_user.id)

    pending_items = [item for item in cart_items if item.status == "pending"]

    total_quantity = sum(item.quantity for item in pending_items)  

    return jsonify({'count': total_quantity})

def add_cart(request, inventory_uuid=None):
    if request.method == 'POST':
        if inventory_uuid:
            try:
                uuid_obj = UUID(str(inventory_uuid)) 
                inventory = inventory_service.get_one(uuid=str(uuid_obj))  
            except ValueError:
                return render_template('404.html'), 404

            if not inventory:
                return render_template('404.html'), 404
            
            user_id = request.form['user_id'].strip().lower()
            quantity = int(request.form['quantity'].strip()) 

            existing_cart_item = cart_service.get_one(user_id=user_id, inventory_id=inventory.id, status="pending")

            pending_cart_items = cart_service.get(user_id=user_id, status="pending")
            total_pending_quantity = sum(item.quantity for item in pending_cart_items if item.inventory_id == inventory.id)

            if existing_cart_item:
                new_quantity = total_pending_quantity + quantity
                
                if new_quantity > inventory.quantity:
                    return jsonify({
                        'success': False,
                        'message': f"⚠️ Not enough stock for {inventory.title}. Available: {inventory.quantity}, Requested: {new_quantity}."
                    }), 400
                
                cart_service.update(existing_cart_item.id, quantity=new_quantity)
            else:
                if total_pending_quantity + quantity > inventory.quantity:
                    return jsonify({
                        'success': False,
                        'message': f"⚠️ Not enough stock for {inventory.title}. Available: {inventory.quantity}, Requested: {total_pending_quantity + quantity}."
                    }), 400

                cart_service.create(
                    user_id=user_id,
                    inventory_id=inventory.id,
                    quantity=quantity,
                    status="pending" 
                )

            return jsonify({
                'success': True,
                'message': f"✅ {inventory.title} has been added to your borrow cart! 🛒 You can continue browsing or <a href='{url_for('main.viewCart')}' class='text-primary'>go to your cart</a>.",
                'inventory_uuid': inventory.uuid  
            }), 200

    return jsonify({'error': True, 'message': 'Create method must be POST.'}), 405

def update_cart_quantity():
    data = request.get_json()
    cart_id = data.get('cart_id')
    new_quantity = int(data.get('quantity'))

    cart_item = cart_service.get_one(id=cart_id, user_id=current_user.id)

    if not cart_item:
        return jsonify({'success': False, 'message': 'Cart item not found.'}), 404

    if new_quantity < 1:
        return jsonify({'success': False, 'message': 'Quantity must be at least 1.'}), 400

    if new_quantity > cart_item.inventory_item.quantity:
        return jsonify({'success': False, 'message': 'Not enough stock available.'}), 400

    cart_service.update(cart_id, quantity=new_quantity)

    return jsonify({'success': True, 'message': 'Cart updated successfully.'}), 200

def remove_cart_item():
    data = request.get_json()
    cart_id = data.get('cart_id')

    cart_item = cart_service.get_one(id=cart_id, user_id=current_user.id)

    if not cart_item:
        return jsonify({'success': False, 'message': 'Cart item not found.'}), 404

    cart_service.delete(cart_id)

    return jsonify({'success': True, 'message': 'Item removed from cart.'}), 200
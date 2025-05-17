from flask import  request,render_template
from flask import jsonify
import os
import uuid
from datetime import datetime
from sqlalchemy.orm import joinedload
from flask_login import current_user
from config import Config
from app.models.inventory_models import Inventory
from app.models.borrowing_models import Borrowing
from app.models.borrowing_details_model import BorrowingDetails
from app.services.services import CRUDService
from app.models.borrowing_status_model import BorrowedItemStatus
from app.models.cart_models import Cart
inventory_service = CRUDService(Inventory)
borrowing_service = CRUDService(Borrowing)
cancel_service = CRUDService(BorrowingDetails)
borrow_status = CRUDService(BorrowedItemStatus)
cart_services = CRUDService(Cart)

def borrowings(request, item_uuid=None):
  
   if request.method == 'GET':
        now = datetime.utcnow()
      
        borrowing_list = Borrowing.query.all()  
        borrowings = [] 
        for borrowing in borrowing_list:
            borrowing.inventory_item = borrowing.cart_items[0].inventory_item if borrowing.cart_items else None  

            if borrowing.end_date:
                delta_days = (borrowing.end_date.date() - now.date()).days
                
                if delta_days >= 0:
                    borrowing.days_remaining = delta_days
                    borrowing.days_late = 0
                else:
                    borrowing.days_remaining = 0
                    borrowing.days_late = abs(delta_days)  # Correctly store overdue days
            else:
                borrowing.days_remaining = None
                borrowing.days_late = None


            if borrowing.get_cart_items:
               borrowing.inventory_titles = [
                    f"{cart_item.inventory_item.title.capitalize()} (Qty: {cart_item.quantity})"
                    for cart_item in borrowing.cart_items if cart_item.inventory_item
                ]
               
               
            else:
                borrowing.inventory_titles = [] 
         

        return render_template('admin/borrowing.html', borrowings=borrowing_list)
 
 
def borrowing_fetch(id):
    now = datetime.utcnow()
    borrowing = Borrowing.query.get_or_404(id)

    # Extract items from cart
    items = []
    for cart_item in borrowing.cart_items:
        item = cart_item.inventory_item
        if item:
            items.append({
                'cart_id': cart_item.id,
                'item_id': item.id, 
                'title': item.title,
                'quantity': cart_item.quantity
            })

    return jsonify({
        'id': borrowing.id,
        'items': items,
       })
    
def borrowings_status(request, borrowing_id=None):
    if request.method != 'PUT':
        return jsonify({'error': True, 'message': 'Invalid Method'}), 400

    borrowing = borrowing_service.get_one(id=borrowing_id)

    if not borrowing:
        return jsonify({'success': False, 'message': 'Borrowing record not found'}), 404

    data = request.json
    new_status = data.get("status")

    if new_status == "approved":
        for cart_item in borrowing.cart_items:
            inventory = inventory_service.get_one(id=cart_item.inventory_id)

            if not inventory:
                return jsonify({
                    'success': False,
                    'message': f'Inventory ID {cart_item.inventory_id} not found'
                }), 404

            if inventory.quantity < cart_item.quantity:
                return jsonify({
                    'success': False,
                    'message': f"⚠️ Not enough stock for {inventory.title}. Available: {inventory.quantity}, Requested: {cart_item.quantity}."
                }), 400

            inventory.quantity -= cart_item.quantity

            if inventory.quantity == 0:
                inventory.status = 'borrowed'
            else:
                inventory.status = 'available'

            inventory_service.update(inventory)

    borrowing_service.update(borrowing.id, status=new_status)

    return jsonify({'success': True, 'message': 'Borrowing request updated successfully'}), 200

def borrowings_done(request, borrowing_id=None):
    if request.method == 'PUT':
        now = datetime.utcnow()
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

        if new_status == "completed":
            borrowing.return_date = now
            
        borrowing_service.update(borrowing.id, status=new_status, return_date=borrowing.return_date)
        return jsonify({'success': True, 'message': 'Borrowing completed'}), 200
    return jsonify({'error': False, 'message': 'Invalid Method'}), 400


def borrowings_done_status(request):
    if request.method == 'PUT':
        now = datetime.utcnow()
        data = request.get_json()
        borrowing_id = data.get('borrowing_id')
        returned_ids = data.get('returned_items', [])
        unreturned_ids = data.get('unreturned_items', [])
        
        borrowing = borrowing_service.get_one(id=borrowing_id)

        if not borrowing:
            return jsonify({'success': False, 'message': 'Borrowing record not found'}), 404
        
        if returned_ids:
            for cart_id in returned_ids:
                cart_item = cart_services.get_one(id=cart_id)
                if cart_item:
                    item_status = BorrowedItemStatus.query.filter_by(
                        borrowing_id=borrowing.id,
                        inventory_item_id=cart_item.inventory_id
                    ).first()

                    if item_status:
                        borrow_status.update(item_status.id, is_returned=True, return_date=now)
                    else:
                        new_item_status = borrow_status.create(
                            borrowing_id=borrowing.id,
                            inventory_item_id=cart_item.inventory_id,
                            quantity=cart_item.quantity,
                            is_returned=True,
                            return_date=now,
                            marked_by_id=current_user.id
                        )
                        if not new_item_status:
                            return jsonify({'success': False, 'message': f"Failed to create status for cart item {cart_id}"}), 500

                    # ✅ Always update inventory when item is returned
                    inventory = inventory_service.get_one(id=cart_item.inventory_id)
                    if inventory:
                        inventory.quantity += cart_item.quantity
                        inventory.status = 'available'
                        inventory_service.update(inventory)

        if unreturned_ids:
            
            for cart_id in unreturned_ids:
                 cart_item = cart_services.get_one(id=cart_id)
                 if cart_item:
                    item_status = BorrowedItemStatus.query.filter_by(
                        borrowing_id=borrowing.id,
                        inventory_item_id=cart_item.inventory_id
                    ).first()

                    if item_status:
                        item_status.is_returned = True
                        item_status.return_date = now
                        borrow_status.update(item_status.id, is_returned=True, return_date=now)
                    else:
                        new_item_status = borrow_status.create(
                            borrowing_id=borrowing.id,
                            inventory_item_id=cart_item.inventory_id,
                            quantity=cart_item.quantity,
                            is_returned=False,
                            marked_by_id=current_user.id,
                            return_date=None
                        )
                        if not new_item_status:
                            return jsonify({'success': False, 'message': f"Failed to create status for cart item {cart_id}"}), 500

        new_status = data.get("status")
        if new_status == "completed":
            borrowing.return_date = now  
        borrowing_service.update(borrowing.id, status=new_status, return_date=borrowing.return_date)
        
        return jsonify({'success': True, 'message': 'Borrowing completed'}), 200

    return jsonify({'error': False, 'message': 'Invalid Method'}), 400


def borrowings_cancel_reason(request, borrowing_id=None):
    if request.method == 'PUT':
        borrowing = borrowing_service.get_one(id=borrowing_id)

        if not borrowing:
            return jsonify({'success': False, 'message': 'Borrowing record not found'}), 404
        
        data = request.json
        new_status = data.get("status")
        reason = data.get("reason")
        if new_status != "cancelled":
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        for cart_item in borrowing.cart_items:
            inventory = inventory_service.get_one(id=cart_item.inventory_id)  

            if not inventory:
                return jsonify({'success': False, 'message': f'Inventory ID {cart_item.inventory_id} not found'}), 404

            inventory.quantity += cart_item.quantity

            if inventory.quantity > 0:
                inventory.status = 'available'

            inventory_service.update(inventory)

        
        borrowing_service.update(borrowing.id, status=new_status)
        cancel_service.create(borrowing_id=borrowing.id, cancel_reason=reason)
        return jsonify({'success': True, 'message': 'Borrowing request canceled'}), 200
    return jsonify({'error': False, 'message': 'Invalid Method'}), 400

def borrowings_cancel(request, borrowing_id=None):
    if request.method == 'PUT':
        borrowing = borrowing_service.get_one(id=borrowing_id)

        if not borrowing:
            return jsonify({'success': False, 'message': 'Borrowing record not found'}), 404
        
        data = request.json
        new_status = data.get("status")
        if new_status != "cancelled":
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        for cart_item in borrowing.cart_items:
            inventory = inventory_service.get_one(id=cart_item.inventory_id)  

            if not inventory:
                return jsonify({'success': False, 'message': f'Inventory ID {cart_item.inventory_id} not found'}), 404

            inventory.quantity += cart_item.quantity

            if inventory.quantity > 0:
                inventory.status = 'available'

            inventory_service.update(inventory)

        
        borrowing_service.update(borrowing.id, status=new_status)
        cancel_service.create(borrowing_id=borrowing.id)
        return jsonify({'success': True, 'message': 'Borrowing request canceled'}), 200
    return jsonify({'error': False, 'message': 'Invalid Method'}), 400
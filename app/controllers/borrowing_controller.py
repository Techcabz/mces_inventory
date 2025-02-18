from flask import  request,render_template
from flask import jsonify
import os
import uuid
from datetime import datetime

from config import Config
from app.models.inventory_models import Inventory
from app.models.borrowing_models import Borrowing
from app.models.borrowing_details_model import BorrowingDetails
from app.services.services import CRUDService

inventory_service = CRUDService(Inventory)
borrowing_service = CRUDService(Borrowing)
cancel_service = CRUDService(BorrowingDetails)

def borrowings(request, item_uuid=None):
   if request.method == 'GET':
        borrowing_list = borrowing_service.get()
        now = datetime.utcnow()

        for borrowing in borrowing_list:
            if borrowing.end_date:
                days_remaining = (borrowing.end_date - now).days
                borrowing.days_remaining = max(0, days_remaining)  
                borrowing.days_late = max(0, -days_remaining) 
            else:
                borrowing.days_remaining = None
                borrowing.days_late = None

        return render_template('admin/borrowing.html', borrowings=borrowing_list)
    
def borrowings_status(request, borrowing_id=None):
    if request.method == 'PUT':
        borrowing = borrowing_service.get_one(id=borrowing_id)

        if not borrowing:
            return jsonify({'success': False, 'message': 'Borrowing record not found'}), 404
        
        data = request.json
        new_status = data.get("status")

        borrowing_service.update(borrowing.id, status=new_status)
        return jsonify({'success': True, 'message': 'Borrowing request approved'}), 200
    return jsonify({'error': False, 'message': 'Invalid Method'}), 400

def borrowings_done(request, borrowing_id=None):
    if request.method == 'PUT':
        borrowing = borrowing_service.get_one(id=borrowing_id)

        if not borrowing:
            return jsonify({'success': False, 'message': 'Borrowing record not found'}), 404
        
        data = request.json
        new_status = data.get("status")
        inventory_id = data.get("inventory_id")
        quantity = int(data.get("quantity"))
        inventory = inventory_service.get_one(id=inventory_id) 

        # add quantity from inventory
        inventory.quantity += quantity
        inventory_service.update(inventory)
            
        borrowing_service.update(borrowing.id, status=new_status)
        return jsonify({'success': True, 'message': 'Borrowing request approved'}), 200
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
        
        borrowing_service.update(borrowing.id, status=new_status)
        cancel_service.create(borrowing_id=borrowing.id, cancel_reason=reason)
        return jsonify({'success': True, 'message': 'Borrowing request canceled'}), 200
    return jsonify({'error': False, 'message': 'Invalid Method'}), 400
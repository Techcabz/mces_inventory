from flask import  request,render_template
from flask import jsonify
import os
import uuid
import time
from config import Config
from app.models.inventory_models import Inventory
from app.models.borrowing_models import Borrowing
from app.services.services import CRUDService

inventory_service = CRUDService(Inventory)
borrowing_service = CRUDService(Borrowing)

def borrowings(request, item_uuid=None):
    if request.method == 'GET':
        borrowing_list = borrowing_service.get()
        return render_template('admin/borrowing.html',borrowings=borrowing_list)
    
def borrowings_approval(request, borrowing_id=None):
    if request.method == 'PUT':
        borrowing = borrowing_service.get_one(id=borrowing_id)

        if not borrowing:
            return jsonify({'success': False, 'message': 'Borrowing record not found'}), 404
        
        data = request.json
        new_status = data.get("status")

        if new_status != "approved":
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        borrowing_service.update(borrowing.id, status=new_status)
        return jsonify({'success': True, 'message': 'Borrowing request approved'}), 200
    return jsonify({'error': False, 'message': 'Invalid Method'}), 400

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
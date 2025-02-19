from flask import  request,render_template
from flask import jsonify
from app.models.inventory_models import Inventory
from app.models.user_models import User
from app.services.services import CRUDService

inventory_service = CRUDService(Inventory)
user_service = CRUDService(User)

def dashboard_set():
    
    pending_count = inventory_service.count(status='pending')
    approved_count = inventory_service.count(status='approved')
    user_count = user_service.count()
    
    return render_template(
        'admin/dashboard.html',
        pending_count=pending_count,
        approved_count=approved_count,
        user_count=user_count
    )
  

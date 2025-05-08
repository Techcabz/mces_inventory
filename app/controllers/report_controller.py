from flask import  request,render_template
from app.models.borrowing_models import Borrowing
from datetime import datetime, timedelta
from sqlalchemy import or_, and_

from app.models.inventory_models import Inventory
from app.models.borrowing_models import Borrowing
from app.models.borrowing_details_model import BorrowingDetails
from app.services.services import CRUDService

inventory_service = CRUDService(Inventory)
borrowing_service = CRUDService(Borrowing)
cancel_service = CRUDService(BorrowingDetails)

def report(request):
    borrowing_list = Borrowing.query.all() 
    borrowings = [] 
    for borrowing in borrowing_list:
        borrowing.inventory_item = borrowing.cart_items[0].inventory_item if borrowing.cart_items else None  

          
        if borrowing.get_cart_items:
            borrowing.inventory_titles = [
                f"{cart_item.inventory_item.title.capitalize()} (Qty: {cart_item.quantity})"
                for cart_item in borrowing.cart_items if cart_item.inventory_item
            ]
        else:
            borrowing.inventory_titles = []
    return render_template('admin/reports.html', borrowings=borrowing_list)

def get_return_status_report():
    """
    Returns a report of returned and unreturned items with their details
    """
    # Get all borrowings with their cart items
    borrowings = Borrowing.query.all()
    
    report_data = []
    
    for borrowing in borrowings:
        # Get all cart items for this borrowing
        cart_items = borrowing.get_cart_items()
        
        for item in cart_items:
            inventory_item = item.inventory_item
            is_returned = borrowing.return_date is not None
            
            report_data.append({
                "reference_number": borrowing.reference_number,
                "borrower": borrowing.user.username,  # Assuming User model has username
                "item_title": inventory_item.title,
                "item_model": inventory_item.property_no,  # Assuming property_no is the model number
                "inv_tag": inventory_item.inv_tag,
                "start_date": borrowing.start_date.strftime('%Y-%m-%d'),
                "end_date": borrowing.end_date.strftime('%Y-%m-%d') if borrowing.end_date else None,
                "return_date": borrowing.return_date.strftime('%Y-%m-%d') if borrowing.return_date else None,
                "status": "Returned" if is_returned else "Not Returned",
                "quantity": item.quantity
            })
    
    return report_data


def get_borrower_report(user_id=None):
    """
    Returns a report filtered by borrower (user)
    If user_id is None, returns all borrowers' data
    """
    query = Borrowing.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    borrowings = query.all()
    
    report_data = []
    
    for borrowing in borrowings:
        cart_items = borrowing.get_cart_items()
        
        for item in cart_items:
            inventory_item = item.inventory_item
            
            report_data.append({
                "borrower_id": borrowing.user_id,
                "borrower_name": borrowing.user.username,  # Adjust based on your User model
                "borrower_email": borrowing.user.email,    # Adjust based on your User model
                "reference_number": borrowing.reference_number,
                "item_title": inventory_item.title,
                "start_date": borrowing.start_date.strftime('%Y-%m-%d'),
                "end_date": borrowing.end_date.strftime('%Y-%m-%d') if borrowing.end_date else None,
                "status": borrowing.status,
                "quantity": item.quantity
            })
    
    return report_data

def get_item_report(inventory_id=None):
    """
    Returns a report filtered by specific inventory item
    If inventory_id is None, returns all items' data
    """
    # Get all cart items that have been borrowed
    query = Cart.query.join(borrowing_cart).join(Borrowing)
    
    if inventory_id:
        query = query.filter_by(inventory_id=inventory_id)
    
    cart_items = query.all()
    
    report_data = []
    
    for item in cart_items:
        borrowing = item.borrowed_by[0]  # Get the first borrowing (assuming one borrowing per cart item)
        inventory_item = item.inventory_item
        
        report_data.append({
            "item_id": inventory_item.id,
            "item_title": inventory_item.title,
            "inv_tag": inventory_item.inv_tag,
            "model_number": inventory_item.property_no,
            "category": inventory_item.category.name,
            "borrower": borrowing.user.username,
            "start_date": borrowing.start_date.strftime('%Y-%m-%d'),
            "end_date": borrowing.end_date.strftime('%Y-%m-%d') if borrowing.end_date else None,
            "return_date": borrowing.return_date.strftime('%Y-%m-%d') if borrowing.return_date else None,
            "status": borrowing.status,
            "quantity_borrowed": item.quantity,
            "current_stock": inventory_item.quantity
        })
    
    return report_data

def get_date_range_report(start_date=None, end_date=None, return_date_filter=None):
    """
    Returns a report filtered by date ranges
    - start_date: filter borrowings that started in this range
    - end_date: filter borrowings that should be returned by this range
    - return_date_filter: filter by actual return date
    """
    query = Borrowing.query
    
    if start_date:
        query = query.filter(Borrowing.start_date >= start_date)
    if end_date:
        query = query.filter(Borrowing.end_date <= end_date)
    if return_date_filter:
        query = query.filter(Borrowing.return_date == return_date_filter)
    
    borrowings = query.all()
    
    report_data = []
    
    for borrowing in borrowings:
        cart_items = borrowing.get_cart_items()
        
        for item in cart_items:
            inventory_item = item.inventory_item
            
            report_data.append({
                "reference_number": borrowing.reference_number,
                "borrower": borrowing.user.username,
                "item_title": inventory_item.title,
                "start_date": borrowing.start_date.strftime('%Y-%m-%d'),
                "end_date": borrowing.end_date.strftime('%Y-%m-%d') if borrowing.end_date else None,
                "return_date": borrowing.return_date.strftime('%Y-%m-%d') if borrowing.return_date else None,
                "days_borrowed": (datetime.utcnow() - borrowing.start_date).days if not borrowing.return_date else 
                                (borrowing.return_date - borrowing.start_date).days,
                "status": borrowing.status,
                "quantity": item.quantity
            })
    
    return report_data
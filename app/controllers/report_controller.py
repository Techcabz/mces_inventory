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
    inventory_list = inventory_service.get() 

    borrowings = [] 
    for borrowing in borrowing_list:
        borrowing.inventory_item = borrowing.cart_items[0].inventory_item if borrowing.cart_items else None  

        # Adding item titles to the borrowing object
        if borrowing.get_cart_items:
            borrowing.inventory_titles = [
                f"{cart_item.inventory_item.title.capitalize()} (Qty: {cart_item.quantity})"
                for cart_item in borrowing.cart_items if cart_item.inventory_item
            ]
        else:
            borrowing.inventory_titles = []

        # Adding more item details to each borrowing
        borrowing.item_details = []
        for cart_item in borrowing.cart_items:
            inventory_item = cart_item.inventory_item
            if inventory_item:
                item_detail = {
                    "title": inventory_item.title,
                    "inv_tag": inventory_item.inv_tag,
                    "property_no": inventory_item.property_no,
                    "date_acquired": inventory_item.date_acquired.strftime('%Y-%m-%d') if inventory_item.date_acquired else None,
                    "cost": float(inventory_item.cost),
                    "quantity": cart_item.quantity,
                    "status": inventory_item.status,
                    "officer": inventory_item.officer,
                    "image": inventory_item.image,
                    "description": inventory_item.description,
                }
                borrowing.item_details.append(item_detail)

    return render_template('admin/reports.html', borrowings=borrowing_list, inventories=inventory_list)

from flask import  request,render_template
from app.models.borrowing_models import Borrowing
from datetime import datetime, timedelta
from sqlalchemy import or_, and_

from app.models.inventory_models import Inventory
from app.models.borrowing_models import Borrowing
from app.models.borrowing_details_model import BorrowingDetails
from app.services.services import CRUDService
from app.models.borrowing_status_model import BorrowedItemStatus  
inventory_service = CRUDService(Inventory)
borrowing_service = CRUDService(Borrowing)
cancel_service = CRUDService(BorrowingDetails)

def report(request):
    borrowing_list = Borrowing.query.all()
    inventory_list = inventory_service.get()

    borrowers_set = set()
    for b in borrowing_list:
        if b.user and b.user.fullname:
            borrowers_set.add(b.user.fullname)

    unique_borrowers = sorted(borrowers_set)
    
    inventory_set = set()
    for b in inventory_list:
        if b.officer:
            inventory_set.add(b.officer)

    unique_inv = sorted(inventory_set)
    
    report_rows = []

    for borrowing in borrowing_list:
        # Get unique officers
        officers = []
        for cart_item in borrowing.cart_items:
            officer = cart_item.inventory_item.officer
            if officer and officer not in officers:
                officers.append(officer)
        officer_string = ', '.join(officers)

        for cart_item in borrowing.cart_items:
            inventory_item = cart_item.inventory_item
            if not inventory_item:
                continue

            # Get item status
            item_status = BorrowedItemStatus.query.filter_by(
                borrowing_id=borrowing.id,
                inventory_item_id=inventory_item.id
            ).first()

            report_rows.append({
                'item_title': inventory_item.title,
                'quantity': cart_item.quantity,
                'borrower': borrowing.user.fullname,
                'officer': officer_string,
                'status': 'Returned' if item_status and item_status.is_returned else 'Unreturned',
                'return_date': item_status.return_date.strftime('%b %d, %Y') if item_status and item_status.return_date else None,
                'borrow_date': borrowing.start_date.strftime('%b %d, %Y'),
            })
            
        print(borrowing_list)

    return render_template('admin/reports.html', report_rows=report_rows, inventories=inventory_list, borrowings=borrowing_list, unique_borrowers=unique_borrowers, unique_inv=unique_inv)

from flask import  request,render_template
from flask import jsonify
from app.models.inventory_models import Inventory
from app.models.user_models import User
from app.services.services import CRUDService
from datetime import datetime
import calendar
from collections import defaultdict

from app.models.borrowing_models import Borrowing
inventory_service = CRUDService(Inventory)
user_service = CRUDService(User)
user_services = CRUDService(User)
borrow_services= CRUDService(Borrowing)

def dashboard_set():
    
     # Fetch counts
    pending_count = borrow_services.count(status='pending')
    approved_count = borrow_services.count(status='approved')
    total_borrowing_count = borrow_services.count()  
    user_pending = user_service.count(status=0) 
    user_count = user_service.count()
    
    return render_template(
        'admin/dashboard.html',
        pending_count=pending_count,
        approved_count=approved_count,
        total_borrowing_count=total_borrowing_count,  
        user_count=user_count,
        user_pending=user_pending

    )


def borrowing_chart_data():
    borrowings = borrow_services.get()  # Fetch all borrowing records
    
    # Dictionary to store counts for each month
    monthly_data = defaultdict(lambda: {"cancelled": 0, "completed": 0})

    for borrow in borrowings:
        if borrow.status in ["cancelled", "completed"]:  # Ensure correct statuses
            month = borrow.created_at.month  # Extract month as number (1-12)
            year = borrow.created_at.year  # Extract year

            # Convert month number to full month name
            month_name = f"{calendar.month_name[month]} {year}"  

            if borrow.status == "cancelled":
                monthly_data[month_name]["cancelled"] += 1
            elif borrow.status == "completed":
                monthly_data[month_name]["completed"] += 1

    # Sort by date (keeping full month names)
    categories = sorted(monthly_data.keys(), key=lambda x: (int(x.split()[1]), list(calendar.month_name).index(x.split()[0])))

    cancelled_counts = [monthly_data[month]["cancelled"] for month in categories]
    completed_counts = [monthly_data[month]["completed"] for month in categories]

    return jsonify({
        "categories": categories,  # Now full month names!
        "cancelled": cancelled_counts,
        "completed": completed_counts
    })
  

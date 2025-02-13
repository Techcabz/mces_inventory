from flask import request, render_template, jsonify
from app.models.inventory_models import Inventory
from app.models.category_models import Category
from app.models.borrowing_models import Borrowing
from app.services.services import CRUDService
from app.utils.file_utils import get_inventory_image
from uuid import UUID 
from datetime import datetime

inventory_service = CRUDService(Inventory)
borrowing_service = CRUDService(Borrowing)
category_service = CRUDService(Category)

def items(request, inventory_uuid=None):  
    
    if request.method == 'GET':
       
        if inventory_uuid:
            try:
                uuid_obj = UUID(str(inventory_uuid)) 
               
                inventory = inventory_service.get_one(uuid=str(uuid_obj)) 
               
            except ValueError:
                return render_template('404.html'), 404

            if not inventory:
                return render_template('404.html'), 404

            inventory_data = inventory.serialize()
            inventory_data['image_url'] = get_inventory_image(inventory.image)
            inventory_data['uuid'] = inventory.uuid
            
            return render_template('user/single_item.html', inventory=inventory_data)

        item_list = inventory_service.get()
        categories = category_service.get()
        
        category_items = {category.name.lower(): [] for category in categories}

        for item in item_list:
            item.image_url = get_inventory_image(item.image)
            category_name = item.category.name.lower()
            
            if category_name in category_items:
                category_items[category_name].append(item)
            else:
                category_items[category_name] = [item]

            
        return render_template('user/dashboard.html',  categories=categories, category_items=category_items)
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
            start_date_str = request.form['start_date'].strip().lower()
            end_date_str = request.form['end_date'].strip().lower()
            inventory_id = inventory.id

            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                today = datetime.today().date()

                if start_date < today:
                    return jsonify({'success': False, 'message': 'Start date cannot be in the past.'}), 400
                
                if end_date <= start_date:
                    return jsonify({'success': False, 'message': 'End date must be after the start date.'}), 400

            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

            if inventory.quantity < quantity:
                return jsonify({'success': False, 'message': 'Not enough quantity available for borrowing.'}), 400

            # Deduct quantity from inventory
            inventory.quantity -= quantity
            inventory_service.update(inventory)
            
            borrowing_service.create(user_id=user_id,inventory_id=inventory_id,start_date=start_date,end_date=end_date,quantity=quantity )

            return jsonify({
            'success': True,
            'message': 'Your borrowing request has been submitted and is pending approval from the admin.'
            }), 200
        return jsonify({'success': False, 'message': 'Create method must be POST.'}), 405
    
def search_items():
    query = request.args.get("q", "").strip().lower()

    if not query:
        # If no query, return all items grouped by category
        items = inventory_service.get()
        return jsonify([
            {
                "title": item.title.capitalize(),
                "image_url": get_inventory_image(item.image),
                "quantity": item.quantity,
                "status": item.status.capitalize(),
                "category": item.category.name.capitalize() if item.category else "Uncategorized",
            }
            for item in items
        ])

    # If query exists, filter items
    items = inventory_service.get()
    filtered_items = [
        {
            "title": item.title.capitalize(),
            "image_url": get_inventory_image(item.image),
            "quantity": item.quantity,
            "status": item.status.capitalize(),
            "category": item.category.name.capitalize() if item.category else "Uncategorized",
        }
        for item in items if query in item.title.lower() or query in (item.category.name.lower() if item.category else "")
    ]

    return jsonify(filtered_items)

from flask import  request,render_template
from flask import jsonify
from app.models.inventory_models import Inventory
from app.models.category_models import Category
from app.services.services import CRUDService
from app.utils.validation_utils import Validation

inventory_service = CRUDService(Inventory)
category_service = CRUDService(Category)

def inventories(request, inventory_id=None):
    if request.method == 'GET':
        if inventory_id:
            # Fetch a single inventory item by ID
            inventory = inventory_service.get_one(id=inventory_id)
            if not inventory:
                return jsonify({'success': False, 'message': 'Inventory not found'}), 404
            
           
            return jsonify(inventory.serialize()), 200  # Ensure `serialize()` is implemented in your model

        inventory_list = inventory_service.get()
        print(inventory_list)
        categories = category_service.get()
        
        return render_template('admin/inventory.html', inventories=inventory_list, categories=categories)
    elif request.method == 'POST':
        title = request.form.get('title', '').lower()
        category_id = request.form.get('category_id', '')
        property_no = request.form.get('property_no', '').lower()
        date_acquired = request.form.get('date_acquired', '')
        cost = request.form.get('cost', '')
        fund_source = request.form.get('fund_source', '').lower()
        officer = request.form.get('officer', '').lower()
        school = request.form.get('school', '').lower()
        qty = request.form.get('qty', '')
        
        if not all([title, category_id, property_no, date_acquired, cost, fund_source, officer, school, qty]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        if not Validation.is_valid_name(title):
            return jsonify({'success': False, 'message': 'Title must contain only letters and spaces.'}), 400

        if Validation.has_repeated_characters(title):
            return jsonify({'success': False, 'message': 'Title must not have three or more consecutive repeated characters.'}), 400

        if not Validation.is_valid_number(qty):
            return jsonify({'success': False, 'message': 'Quantity must be a positive integer.'}), 400

        # Create and save inventory
        inventory_service.create( title=title,
            category_id=category_id,
            property_no=property_no,
            date_acquired=date_acquired,
            cost=cost,
            fund_source=fund_source,
            officer=officer,
            school=school,
            quantity=qty)
        return jsonify({'success': True, 'message': 'Inventory item added successfully!'}), 201
    elif request.method == 'PUT':
        if inventory_id:
          
            title = request.form.get('title', '').lower()
            category_id = request.form.get('category_id', '')
            property_no = request.form.get('property_no', '').lower()
            date_acquired = request.form.get('date_acquired', '')
            cost = request.form.get('cost', '')
            fund_source = request.form.get('fund_source', '').lower()
            officer = request.form.get('officer', '').lower()
            school = request.form.get('school', '').lower()
            qty = request.form.get('qty', '')
       
            if not all([title, category_id, property_no, date_acquired, cost, fund_source, officer, school, qty]):
                return jsonify({'success': False, 'message': 'All fields are required.'}), 400

            if not Validation.is_valid_name(title):
                return jsonify({'success': False, 'message': 'Title must contain only letters and spaces.'}), 400

            if Validation.has_repeated_characters(title):
                return jsonify({'success': False, 'message': 'Title must not have three or more consecutive repeated characters.'}), 400

            if not Validation.is_valid_number(qty):
                return jsonify({'success': False, 'message': 'Quantity must be a positive integer.'}), 400

            # # Create and save inventory
            inventory_service.update(inventory_id, title=title,
                category_id=category_id,
                property_no=property_no,
                date_acquired=date_acquired,
                cost=cost,
                fund_source=fund_source,
                officer=officer,
                school=school,
                quantity=qty)
            return jsonify({'success': True, 'message': 'Inventory item added successfully!'}), 201
        return jsonify({'success': False, 'message': 'Inventory not found'}), 404
    elif request.method == 'DELETE':
        id = request.form['id']
        if not id:
            return jsonify({'success': False, 'message': 'Inventory ID is required.'}), 400

        existing_inventory = inventory_service.get_one(id=id)
        if not existing_inventory:
            return jsonify({'success': False, 'message': 'Inventory not found.'}), 404

        delete_success = inventory_service.delete(id)
        if delete_success:
            return jsonify({'success': True, 'message': 'Inventory deleted successfully!'}), 200
        return jsonify({'success': False, 'message': 'Error deleting inventory.'}), 500
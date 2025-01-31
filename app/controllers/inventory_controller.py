from flask import  request,render_template
from flask import jsonify
from app.models.inventory_models import Inventory
from app.models.category_models import Category
from app.services.services import CRUDService
from app.utils.validation_utils import Validation

inventory_service = CRUDService(Inventory)
category_service = CRUDService(Category)

def inventories(request):
    if request.method == 'GET':
        inventory_list = inventory_service.get()
        categories = category_service.get()
        return render_template('admin/inventory.html', inventory=inventory_list, categories=categories)
    elif request.method == 'POST':
        title = request.form.get('title', '')
        category_id = request.form.get('category_id', '')
        property_no = request.form.get('property_no', '')
        date_acquired = request.form.get('date_acquired', '')
        cost = request.form.get('cost', '')
        fund_source = request.form.get('fund_source', '')
        officer = request.form.get('officer', '')
        school = request.form.get('school', '')
        qty = request.form.get('qty', '')
        
        if not all([title, category_id, property_no, date_acquired, cost, fund_source, officer, school, qty]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        # Validate title (Only alphabetic & spaces)
        if not Validation.is_valid_name(title):
            return jsonify({'success': False, 'message': 'Title must contain only letters and spaces.'}), 400

        # Validate no three or more consecutive repeated characters in title
        if Validation.has_repeated_characters(title):
            return jsonify({'success': False, 'message': 'Title must not have three or more consecutive repeated characters.'}), 400

        # Validate qty (must be a positive number)
        if not Validation.is_valid_number(qty):
            return jsonify({'success': False, 'message': 'Quantity must be a positive integer.'}), 400


        # # Create and save inventory
       
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
        
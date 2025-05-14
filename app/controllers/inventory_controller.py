from flask import  request,render_template
from flask import jsonify
import os
import uuid
import time
from config import Config
from app.models.inventory_models import Inventory
from app.models.category_models import Category
from app.services.services import CRUDService
from app.utils.validation_utils import Validation
from app.utils.file_utils import get_inventory_image,compress_image

inventory_service = CRUDService(Inventory)
category_service = CRUDService(Category)

def inventories(request, inventory_id=None):
    if request.method == 'GET':
        if inventory_id:
            # Fetch a single inventory item by ID
            inventory = inventory_service.get_one(id=inventory_id)
            if not inventory:
                return jsonify({'success': False, 'message': 'Inventory not found'}), 404
            
            inventory_data = inventory.serialize()
            inventory_data["image_url"] = get_inventory_image(inventory.image)
            return jsonify(inventory_data), 200

        inventory_list = inventory_service.get()
        categories = category_service.get()
        
       
        for item in inventory_list:
            item.image_url = get_inventory_image(item.image)
            
        return render_template('admin/inventory.html', inventories=inventory_list, categories=categories)
    elif request.method == 'POST':
        title = request.form.get('title', '').lower()
        inv_tag = request.form.get('inv_tag', '')
        category_id = request.form.get('category_id', '')
        property_no = request.form.get('property_no', '').lower()
        date_acquired = request.form.get('date_acquired', '')
        cost = request.form.get('cost', '')
        fund_source = request.form.get('fund_source', '').lower()
        officer = request.form.get('officer', '').lower()
        school = request.form.get('school', '').lower()
        qty = request.form.get('qty', '')
        
        if not all([title, category_id,  date_acquired, cost,  officer, qty,inv_tag]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        # if not Validation.is_valid_name(title):
        #     return jsonify({'success': False, 'message': 'Title must contain only letters and spaces.'}), 400
        existing_inventory = inventory_service.get_one(title=title)
        if existing_inventory:
            return jsonify({'success': False, 'message': 'Inventory name is already taken.'}), 400
        
        existing_inv = inventory_service.get_one(inv_tag=inv_tag)
        if existing_inv:
            return jsonify({'success': False, 'message': 'Inventory Tag is existing.'}), 400
        
        if Validation.has_repeated_characters(title):
            return jsonify({'success': False, 'message': 'Title must not have three or more consecutive repeated characters.'}), 400

        if not Validation.is_valid_number(qty):
            return jsonify({'success': False, 'message': 'Quantity must be a positive integer.'}), 400

        file = request.files.get("image")
        filename = None
        if file and Validation.allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()  
            timestamp = int(time.time())  
            unique_id = uuid.uuid4().hex[:8]  
            raw_filename = f"{timestamp}_{unique_id}.{ext}"   
            file_path = os.path.join(Config.UPLOAD_FOLDER, raw_filename)
            file.save(file_path)
            compressed_filename = compress_image(file_path)
            os.remove(file_path)  
            filename = compressed_filename
       
        # Create and save inventory
        inventory_service.create( title=title,
            inv_tag=inv_tag,
            category_id=category_id,
            property_no=property_no,
            date_acquired=date_acquired,
            cost=cost,
            fund_source=fund_source,
            officer=officer,
            school=school,
            quantity=qty,
            image=filename if filename else None )
        return jsonify({'success': True, 'message': 'Inventory item added successfully!'}), 201
    elif request.method == 'PUT':
        if inventory_id:
            inventory = inventory_service.get_one(id=inventory_id)
            title = request.form.get('title', '').lower()
            inv_tag = request.form.get('inv_tag', '')
            category_id = request.form.get('category_id', '')
            property_no = request.form.get('property_no', '').lower()
            date_acquired = request.form.get('date_acquired', '')
            cost = request.form.get('cost', '')
            fund_source = request.form.get('fund_source', '').lower()
            officer = request.form.get('officer', '').lower()
            school = request.form.get('school', '').lower()
            qty = request.form.get('qty', '')
       
            if not all([title, category_id,  date_acquired, cost, officer, qty,inv_tag]):
                return jsonify({'success': False, 'message': 'All fields are required.'}), 400

            # if not Validation.is_valid_name(title):
            #     return jsonify({'success': False, 'message': 'Title must contain only letters and spaces.'}), 400

            if Validation.has_repeated_characters(title):
                return jsonify({'success': False, 'message': 'Title must not have three or more consecutive repeated characters.'}), 400

            if not Validation.is_valid_number(qty):
                return jsonify({'success': False, 'message': 'Quantity must be a positive integer.'}), 400

            file = request.files.get("image")
            filename = inventory.image 
          
            if file and Validation.allowed_file(file.filename):
                ext = file.filename.rsplit(".", 1)[1].lower()  
                timestamp = int(time.time())  
                unique_id = uuid.uuid4().hex[:8]  
                new_filename = f"{timestamp}_{unique_id}.{ext}"  
                file_path = os.path.join(Config.UPLOAD_FOLDER, new_filename)

                # Check if the existing image exists, delete it
                existing_image_path = os.path.join(Config.UPLOAD_FOLDER, inventory.image) if inventory.image else None
                if existing_image_path and os.path.exists(existing_image_path):
                    os.remove(existing_image_path)  # Delete old image

                # Save new file
                file.save(file_path)
                compressed_filename = compress_image(file_path)
                os.remove(file_path)  
                filename = compressed_filename
              
            # Create and save inventory
            inventory_service.update(inventory_id, title=title,inv_tag=inv_tag,
                category_id=category_id,
                property_no=property_no,
                date_acquired=date_acquired,
                cost=cost,
                fund_source=fund_source,
                officer=officer,
                school=school,
                quantity=qty,
                image=filename)
            return jsonify({'success': True, 'message': 'Inventory item updated successfully!'}), 201
        return jsonify({'success': False, 'message': 'Inventory not found'}), 404
    elif request.method == 'DELETE':
        
        if not inventory_id:
            return jsonify({'success': False, 'message': 'Inventory ID is required.'}), 400

        existing_inventory = inventory_service.get_one(id=inventory_id)
        if not existing_inventory:
            return jsonify({'success': False, 'message': 'Inventory not found.'}), 404

        delete_success = inventory_service.delete(inventory_id)
        if delete_success:
            return jsonify({'success': True, 'message': 'Inventory deleted successfully!'}), 200
        return jsonify({'success': False, 'message': 'Error deleting inventory.'}), 500
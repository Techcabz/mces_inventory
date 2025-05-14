from . import admin,web_guard,request,render_template
from app.controllers.categories_controller import categories
from app.controllers.inventory_controller import inventories
from app.controllers.users_controller import update_admin_profile,add_admin_profile,cusers,user_approved,user_disapproved,get_profiles_admin,update_profile_user
from app.controllers.borrowing_controller import borrowings_done_status, borrowing_fetch,borrowings,borrowings_cancel, borrowings_status,borrowings_cancel_reason,borrowings_done
from app.controllers.receipts_controller import receiptGenerate,generate_pdf_custom
from app.controllers.dashboard_controller import dashboard_set,borrowing_chart_data,pending_check_controller
from app.controllers.report_controller import report

# ADMINISTRATOR
@admin.route('/dashboard')
@web_guard
def dashboard():
    return dashboard_set()

@admin.route('/borrowing', methods=['GET', 'POST'])
# @main.route('/borrowing/item/<uuid:item_uuid>', methods=['POST','GET', 'PUT', 'DELETE'])
@web_guard
def borrowing(item_uuid=None):
    return borrowings(request,item_uuid)

@admin.route('/borrowing_fetch/item/<int:id>', methods=['GET'])
@web_guard
def borrowing_fetch_item(id=None):
    return borrowing_fetch(id)


@admin.route("/borrowing/status/<int:borrowing_id>", methods=['GET', 'POST', 'PUT',])
@web_guard
def borrowing_status(borrowing_id=None):
    return borrowings_status(request, borrowing_id)

@admin.route("/borrowing/done/<int:borrowing_id>", methods=['GET', 'POST', 'PUT',])
@web_guard
def borrowing_done(borrowing_id=None):
    return borrowings_done(request, borrowing_id)

@admin.route("/borrowing/done_status", methods=['GET', 'POST', 'PUT',])
@web_guard
def borrowing_done_status():
    return borrowings_done_status(request)


@admin.route("/borrowing/cancel_reason/<int:borrowing_id>", methods=['GET', 'POST', 'PUT',])
@web_guard
def borrowing_cancel_reason(borrowing_id=None):
    return borrowings_cancel_reason(request, borrowing_id)

@admin.route("/borrowing/cancel/<int:borrowing_id>", methods=['GET', 'POST', 'PUT',])
@web_guard
def borrowing_cancel(borrowing_id=None):
    return borrowings_cancel(request, borrowing_id)

@admin.route('/category', methods=['GET', 'POST', 'PUT', 'DELETE'])
@web_guard
def category():
    return categories(request)

@admin.route('/inventory', methods=['GET', 'POST'])
@admin.route('/inventory/<int:inventory_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def inventory(inventory_id=None):
    return inventories(request, inventory_id)

@admin.route('/reports')
@web_guard
def reports():
    return report(request)

@admin.route('/receipts')
@web_guard
def receipts():
    return receiptGenerate()

@admin.route('/receipts-generate')
@web_guard
def generate_pdf():
  return generate_pdf_custom()  
    
@admin.route('/logs')
@web_guard
def logs():
    return render_template('admin/logs.html')

@admin.route('/users', methods=['GET'])
@admin.route('/users/<int:users_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def users(users_id=None):
    return cusers(request,users_id)

@admin.route('/users/approved/<int:users_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def users_approved(users_id=None):
    return user_approved(request,users_id)

@admin.route('/users/disapproved/<int:users_id>', methods=['GET', 'PUT', 'DELETE'])
@web_guard
def user_disapproveds(users_id=None):
    return user_disapproved(request,users_id)


@admin.route('/get_profile_admin/<int:users_id>')
@web_guard
def get_profile_admin(users_id=None):
    return get_profiles_admin(users_id)


@admin.route('/update_profile', methods=['POST'])
@web_guard
def update_profile_users():
    return update_profile_user()

@admin.route('/add_admin_profile', methods=['POST'])
@web_guard
def add_admin_profiles():
    return add_admin_profile()


@admin.route('/update_admin_profile', methods=['POST'])
@web_guard
def update_admin_profiles():
    return update_admin_profile()


@admin.route('/borrowing_chart_data')
@web_guard
def borrowing_chart_datas():
    return borrowing_chart_data()

@admin.route('/pending_checker')
@web_guard
def pending_checker():
    return pending_check_controller()
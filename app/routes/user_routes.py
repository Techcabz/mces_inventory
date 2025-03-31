
from . import main,web_guard_user,request,render_template
from app.controllers.item_controller import update_profiles,get_profiles, items, search_items, users_borrowed, borrowing_status_user, borrow_items
from app.controllers.cart_controller import add_cart, view_cart, get_cart_count, update_cart_quantity, remove_cart_item


# USER DASHBOARD
@main.route('/user/dashboard')
@main.route('/users/item/<uuid:item_uuid>', methods=['POST', 'GET', 'PUT', 'DELETE'])
@web_guard_user
def user_dashboard(item_uuid=None):
    return items(request, item_uuid)

@main.route('/users/borrow_item', methods=['POST', 'GET', 'PUT', 'DELETE'])
@web_guard_user
def borrow_item():
    return borrow_items(request)

@main.route('/user/borrowed')
@main.route('/users/borrowed/item/<uuid:borrow_uuid>', methods=['POST', 'GET', 'PUT', 'DELETE'])
@web_guard_user
def user_borrowed(borrow_uuid=None):
    return users_borrowed(request, borrow_uuid)

@main.route('/users/cart_count')
@web_guard_user
def countCart():
    return get_cart_count()

@main.route('/users/cart_remove', methods=['POST', 'GET', 'PUT', 'DELETE'])
@web_guard_user
def removeCart():
    return remove_cart_item()

@main.route('/users/cart_update', methods=['POST', 'GET', 'PUT', 'DELETE'])
@web_guard_user
def updateCart():
    return update_cart_quantity()

@main.route('/users/view_cart', methods=['POST', 'GET', 'PUT', 'DELETE'])
@web_guard_user
def viewCart():
    return view_cart()

@main.route('/users/cart/<uuid:item_uuid>', methods=['POST', 'GET', 'PUT', 'DELETE'])
@web_guard_user
def addtoCart(item_uuid=None):
    return add_cart(request, item_uuid)

@main.route('/users/borrowed/status/<int:item_id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
@web_guard_user
def borrowings_status_user(item_id=None):
    return borrowing_status_user(request, item_id)

@main.route('/search-items')
def search_item():
    return search_items()

@main.route('/users/get_profile')
@web_guard_user
def get_profile():
    return get_profiles(request)


@main.route('/users/update_profile', methods=['POST'])
@web_guard_user
def update_profile():
    return update_profiles()



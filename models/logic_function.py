import base64
from models import Products, storage, Business, Customers


def populate_homepage(products):
    """Arranges the product in a chronological order
     and places priority for products with a
    registered business"""

    items = []
    image = []
    a_list = []
    b_list = []
    a_list_images = []
    b_list_images = []

    for product in products:
        if product.business_name:
            a_list.append(product)
            a_list_images.append(base64.b64encode(product.product_images).decode('utf-8'))
        else:
            b_list.append(product)
            b_list_images.append(base64.b64encode(product.product_images).decode('utf-8'))
        items.append(product)
        image.append(base64.b64encode(product.product_images).decode('utf-8'))
    a_list.reverse()
    b_list.reverse()
    a_list_images.reverse()
    b_list_images.reverse()
    items = a_list + b_list
    image = a_list_images + b_list_images

    return items, image


def filter_products(group, field):
    """takes in two parameter by which to filter the displayed products"""
    products = storage.all(Products).values()
    filtered_products = []
    if group == 'products':
        for product_n in products:
            if product_n.product_name is not None and product_n.product_name.lower() == field:
                filtered_products.append(product_n)

    elif group == 'business':
        for product_n in products:
            if product_n.name is not None and product_n.name.lower() == field:
                filtered_products.append(product_n)

    elif group == 'state':
        for product_n in products:
            if product_n.business is not None and product_n.business.location.lower() == field:
                filtered_products.append(product_n)
    else:
        return products
    return filtered_products


def user_confirmation(email, password):
    """This checks if a user exists or not and returns an object if it does or None"""
    requested_user = storage.get_obj(attr=email, cls=Business)
    requested_customer = storage.get_obj(attr=email, cls=Customers)
    if requested_user:
        print(requested_user)
        if requested_user.check_password(attempted_password=password):
            return requested_user
    elif requested_customer:
        if requested_customer.check_password(attempted_password=password):
            return requested_customer
    else:
        return None

"""starts the web application"""
import base64
from time import strftime
from flask import render_template, redirect, url_for, request, flash
from models import storage
from models.products import Products
from models.login_form import LoginForm
from models.product_forms import ProductForm
from models.register_forms import BusinessForm, CustomersForm
from models.users import Users
from models.filterform import FilterForm
from models.registered_farm import Business
from models.customers import Customers
from models.reviews import Reviews
from models.reviewForm import ReviewForm
from flask_login import login_user, login_required, current_user, logout_user
from models import app

app.config['SECRET_KEY'] = '23bb8ccb2331455dc681eec4'


def populate_homepage(products):
    """populates the homepage"""

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
            if product_n.business_name is not None and product_n.business_name.lower() == field:
                filtered_products.append(product_n)

    elif group == 'state':
        for product_n in products:
            if product_n.business is not None and product_n.business.location.lower() == field:
                filtered_products.append(product_n)
    else:
        return products
    return filtered_products


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def landing_page():
    """landing page route"""
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """homepage routing"""
    products = storage.all(Products).values()

    items, image = populate_homepage(products)

    form = FilterForm()
    if form.validate_on_submit():
        f_b = form.filter_by.data.lower()
        f_d = form.field.data.lower()
        filter_list = ['state', 'business', 'products']
        if f_d is None or f_b is None:
            return redirect(url_for('home'))
        elif f_b in filter_list:
            return redirect(url_for('filter_product', group=f_b, field=f_d))
        else:
            return redirect(url_for('home'))
    return render_template('homepage.html', form=form, products=items, image=image, zip=zip, mimetype='jpeg',
                           reversed=reversed)


@app.route('/filter/<group>/<field>', methods=['GET', 'POST'], strict_slashes=False)
def filter_product(group, field):
    """Displays products based on state filters"""
    filtered_products = []
    filtered_products = filter_products(group, field)
    item, img_item = populate_homepage(filtered_products)
    form = FilterForm()
    if form.validate_on_submit():
        f_b = form.filter_by.data.lower()
        f_d = form.field.data.lower()
        return redirect(url_for('filter_product', group=f_b, field=f_d))

    return render_template('homepage.html', form=form, products=item, image=img_item, zip=zip, mimetype='jpeg',
                           reversed=reversed)


@app.route('/upload', strict_slashes=False)
def upload():
    """upload a new product"""

    return render_template('new_post.html')


@app.route('/customer', methods=['GET', 'POST'], strict_slashes=False)
def customer():
    """loads the customer register page"""
    form = CustomersForm()
    if form.validate_on_submit():
        n_customer = Customers()

        customer = storage.get(attr=form.username.data, cls=Customers)
        if customer:
            flash('Username already exist')
            return redirect(url_for('customer'))

        customer = storage.get(attr=form.email.data, cls=Customers)
        if customer:
            flash('User with e-mail already exist')
            return redirect(url_for('customer'))

        n_customer.username = form.username.data
        n_customer.email = form.email.data
        n_customer.password = form.password.data
        n_customer.contact = form.contact.data

        file = request.files['profile_pic']
        mimetype = file.mimetype
        n_customer.profile_pic = file.read()

        n_customer.save()
        return redirect(url_for('home'))

    if form.errors != {}:
        for err in form.errors.values():
            flash('There was an error {}'.format(err), category='danger')

    return render_template('customer.html', form=form)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """renders the login template"""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        requested_user = storage.get_obj(attr=form.email.data, cls=Business)
        requested_customer = storage.get_obj(attr=form.email.data, cls=Customers)
        if requested_user:
            print(requested_user)
            if requested_user.check_password(attempted_password=form.password.data):
                login_user(requested_user)
                flash('You are successfully logged in {}'
                      .format(requested_user.business_name), category='success')
                return redirect(url_for('home'))
        if requested_customer:
            if requested_customer.check_password(attempted_password=form.password.data):
                login_user(requested_customer)
                flash('You are successfully logged in {}'
                      .format(requested_customer.username), category='success')
                return redirect(url_for('home'))
        else:
            flash('Wrong email or password', category='danger')
    return render_template('login.html', form=form)


@app.route('/reviews/<string:id>', methods=['GET', 'POST'], strict_slashes=False)
def review(id):
    obj = storage.get_one(cls=Products, id=id)
    review_list = storage.all(cls=Reviews).values()
    comment_list = []

    form = ReviewForm()
    for reviews in review_list:
        if id == reviews.product_id:
            comment_list.append(reviews)

    if form.validate_on_submit():
        user_review = Reviews()
        if type(current_user) == Business:
            user_review.reviewer = current_user.business_name
        elif type(current_user) == Customers:
            user_review.reviewer = current_user.username
        else:
            user_review.reviewer = "Anonymous"
        user_review.product_id = id
        user_review.comment = form.comment.data
        user_review.save()

        return redirect(url_for('review', id=id))

    return render_template('reviews.html', product=obj,
                           image=base64.b64encode(obj.product_images).decode('utf-8'),
                           comments=comment_list, form=form, strftime=strftime, reversed=reversed)


@app.route('/saved_profile', strict_slashes=False)
@login_required
def saved_profile():
    """renders the saved profile template"""
    businesses = storage.all(Business).values()
    product_list = []
    image = []
    for business in businesses:
        if business.business_name == current_user.business_name:
            product_list = business.products.copy()
            for prod in business.products:
                print(prod)
                image.append(base64.b64encode(prod.product_images).decode('utf-8'))
    print(product_list)

    return render_template('saved_profile.html', user=current_user,
                           company_logo=base64.b64encode(current_user.company_logo).decode('utf-8'),
                           product=product_list, image=image, mimetype='jpeg', zip=zip)


@app.route('/profile', methods=['GET', 'POST'], strict_slashes=False)
def profile():
    """ populates the saved profile page """
    form = BusinessForm()
    if form.validate_on_submit():

        check = storage.get(attr=form.email.data, cls=Business)
        if check:
            flash('User with e-mail already exist')
            return redirect(url_for('profile'))

        check = storage.get(attr=form.business_name.data, cls=Business)
        if check:
            flash('Username already exist')
            return redirect(url_for('profile'))
        new_business = Business()

        new_business.business_name = form.business_name.data
        new_business.email = form.email.data
        new_business.password = form.password.data
        new_business.contact = form.contact.data
        new_business.about = form.about.data
        new_business.location = form.location.data
        file = request.files['company_logo']
        mimetype = file.mimetype
        new_business.company_logo = file.read()

        untracked_products = storage.all(cls=Products).values()
        for uproduct in untracked_products:
            if uproduct.users_name == form.business_name.data:
                new_business.products.append(uproduct)

        new_business.save()
        login_user(new_business)
        return redirect(url_for('home'))
    if form.errors != {}:
        for err in form.errors.values():
            flash('There was an error {}'.format(err))

    return render_template('profile.html', form=form)


@app.route('/product', methods=['GET', 'POST'], strict_slashes=False)
def product():
    """uploads a product"""
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Products()

        file = request.files['images']
        mimetype = file.mimetype
        new_product.product_images = file.read()

        new_product.product_name = form.product_name.data
        new_product.farm_name = form.farm_name.data
        new_product.contact = form.contact.data
        new_product.price = form.price.data

        print(type(current_user) is Business)
        print(type(current_user))
        if current_user.is_authenticated and type(current_user) is Business:
            new_product.business = current_user
            print('yuioihgbn')
        else:
            if not storage.get(attr=form.farm_name.data, cls=Users):
                new_user = Users()
                new_user.farm_name = form.farm_name.data
                new_user.state = form.state.data
                new_user.save()

            existing_user = storage.get_obj(attr=form.farm_name.data, cls=Users)
            new_product.users = existing_user

        new_product.save()

        return redirect(url_for('home'))
    if form.errors != {}:
        for err in form.errors.values():
            flash('There was an error {}'.format(err))
    return render_template('new_post.html', form=form, mimetype='png')


@app.route('/logout', strict_slashes=False)
@login_required
def logout():
    """log a user out"""
    logout_user()
    return redirect(url_for('home'))

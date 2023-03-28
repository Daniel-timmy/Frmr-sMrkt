"""starts the web application"""
import base64
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from models import storage
from models.products import Products
from models.login_form import LoginForm
from models.product_forms import ProductForm
from models.register_forms import BusinessForm, CustomersForm
from models.users import Users
from models.registered_farm import Business
from models.customers import Customers
from flask_login import login_user, login_required, current_user, logout_user
from models import app


app.config['SECRET_KEY'] = '23bb8ccb2331455dc681eec4'


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    """homepage routing"""
    products = storage.all(Products).values()
    items = []
    image = []
    for product in products:
        items.append(product)
        image.append(base64.b64encode(product.product_images).decode('utf-8'))
    return render_template('homepage.html', products=items, image=image, zip=zip, mimetype='jpeg', reversed=reversed)


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
    # NEED TO FIX
    form = LoginForm()
    if form.validate_on_submit():
        # THE PROBLEM LIES HERE
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
            flash('Wrong email or password', category='failed')
    return render_template('login.html', form=form)


@app.route('/reviews', strict_slashes=False)
def reviews():

    return render_template('reviews.html')


@app.route('/saved_profile', strict_slashes=False)
@login_required
def saved_profile():
    """renders the saved profile template"""

    return render_template('saved_profile.html', user=current_user, company_logo=base64.b64encode(current_user.company_logo).decode('utf-8'), mimetype='jpeg')


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
        new_user = Users()

        file = request.files['images']
        mimetype = file.mimetype
        new_product.product_images = file.read()

        new_product.product_name = form.product_name.data
        new_product.farm_name = form.farm_name.data
        new_product.contact = form.contact.data
        new_product.price = form.price.data

        # i need to implement this to take care of different
        # product entries with the same farm name and also if the
        #  user already exist do not create
        new_user.farm_name = form.farm_name.data
        new_user.state = form.state.data

        new_product.save()
        new_user.save()

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

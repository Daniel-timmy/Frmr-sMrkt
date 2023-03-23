"""starts the web application"""
import base64
from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from models import storage
from models.products import Products
from models.login_form import LoginForm
from models.product_forms import ProductForm
from models.register_forms import ProfileForm, CustomersForm
from models.users import Users
from models.loggedusers import LoggedUsers
from models.customers import Customers
from flask_login import login_user
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
    return render_template('homepage.html', products=items, image=image, zip=zip, mimetype='jpeg')


@app.route('/upload', strict_slashes=False)
def upload():
    """upload a new product"""

    return render_template('new_post.html')


@app.route('/customer', strict_slashes=False)
def customer():
    """loads the customer register page"""
    form = CustomersForm()
    if form.validate_on_submit():
        n_customer = Customers()
        n_customer.username = form.username.data
        n_customer.email = form.email.data
        n_customer.password = form.password.data
        n_customer.contact = form.contact.data

        file = request.files['profile_pic']
        n_customer.profile_pic = file.read()

        n_customer.save()
        return redirect(url_for('saved_profile'))

    if form.errors != {}:
        for err in form.errors:
            flash('There was an error'.format(err))

    return render_template('customer.html', form=form)


@app.route('/login', strict_slashes=False)
def login():
    """renders the login template"""
    form = LoginForm()
    if form.validate_on_submit():
        requested_user = LoggedUsers.query.filter_by(email=form.email.data).first()
        if requested_user and requested_user.check_password(attempted_password=form.password.data):
            login_user(requested_user)
            flash('You are successfully logged in {}'
                  .format(requested_user.username), category='success')
            return redirect(url_for('home'))
        else:
            flash('Wrong email or password', category='failed')
    return render_template('login.html', form=form)


@app.route('/saved_profile', strict_slashes=False)
def saved_profile():
    """renders the saved profile template"""

    return render_template('saved_profile.html')


@app.route('/profile/', methods=['GET', 'POST'], strict_slashes=False)
def profile():
    """ populates the saved profile page """
    profile_form = ProfileForm()
    return render_template('profile.html', form=profile_form)


@app.route('/product', methods=['GET', 'POST'], strict_slashes=False)
def product():
    """uploads a product"""
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Products()
        new_user = Users()

        file = request.files['images']
        new_product.product_images = file.read()

        new_product.product_name = form.product_name.data
        new_product.farm_name = form.farm_name.data
        new_product.contact = form.contact.data
        new_product.price = form.price.data

        new_user.farm_name = form.farm_name.data
        new_user.state = form.state.data

        new_product.save()
        new_user.save()

        return redirect(url_for('home'))
    if form.errors != {}:
        for err in form.errors:
            flash('There was an error'.format(err))
    return render_template('new_post.html', form=form, mimetype='png')

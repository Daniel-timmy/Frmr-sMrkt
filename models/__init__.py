from models.storage.storage import DBStorage
from models import storage
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from models.products import Products
from models.customers import Customers
from models.users import Users
from models.registered_farm import Business

storage = DBStorage()
storage.reload()

from models.storage.storage import DBStorage
from models.products import Products
from models.loggedusers import LoggedUsers
from models import storage
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

storage = DBStorage()
storage.reload()

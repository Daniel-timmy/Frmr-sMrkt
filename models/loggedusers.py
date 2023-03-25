from models.base_model import FarmModel, Base
from sqlalchemy import Column, String, INTEGER, LargeBinary
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from models import login_manager


@login_manager.user_loader
def load_user(customer_id):
    return LoggedUsers.query.get(customer_id)


class LoggedUsers(FarmModel, Base, UserMixin):
    """class for registered users"""
    __tablename__ = 'loggedUsers'
    __table_args__ = {'extend_existing': True}

    firstname = Column(String(60), nullable=False)
    lastname = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    password_hash = Column(String(60), nullable=False)
    contact = Column(INTEGER, nullable=False)
    farm_name = Column(String(60), nullable=False)
    state = Column(String(60), nullable=False)
    profile_pic = Column(LargeBinary)
    product_base = Column(String(60), nullable=False)
    about = Column(String)
    products = relationship("Products", backref="logged_users", cascade="all, delete, delete-orphan")

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_password):
        """generate a secure password hash"""
        from models import bcrypt
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, attempted_password):
        """confirms if input password matches the hash stored"""
        from models import bcrypt
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

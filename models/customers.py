from models.base_model import FarmModel, Base
from sqlalchemy import Column, String, INTEGER, LargeBinary
from sqlalchemy.orm import relationship
from models import bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(customer_id):
    return Customers.query.get(customer_id)


class Customers(FarmModel, Base, UserMixin):
    """class for registered users"""
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}

    username = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    password_hash = Column(String(60), nullable=False)
    contact = Column(INTEGER, nullable=False)
    profile_pic = Column(LargeBinary)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



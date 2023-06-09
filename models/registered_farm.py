from sqlalchemy.orm import relationship

from models.base_model import FarmModel, Base
from sqlalchemy import Column, String, INTEGER, LargeBinary
from models import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(business_id):
    """loads business accounts"""
    from models import storage
    return storage.get_one(cls=Business, id=business_id)


class Business(FarmModel, Base, UserMixin):
    """Products class"""
    __tablename__ = 'business'
    __table_args__ = {'extend_existing': True}

    name = Column(String, nullable=False)
    company_logo = Column(LargeBinary)
    email = Column(String(60), nullable=False)
    password_hash = Column(String(60), nullable=False)
    contact = Column(INTEGER, nullable=False)
    about = Column(String)
    location = Column(String, nullable=False)
    products = relationship("Products", backref="business", cascade="all, delete, delete-orphan")

    @property
    def password(self):
        """returns the password"""
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

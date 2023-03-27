from sqlalchemy.orm import relationship

from models.base_model import FarmModel, Base
from sqlalchemy import Column, String, INTEGER, LargeBinary


class Business(FarmModel, Base):
    """Products class"""
    __tablename__ = 'business'
    __table_args__ = {'extend_existing': True}

    business_name = Column(String, nullable=False)
    company_logo = Column(LargeBinary)
    email = Column(String(60), nullable=False)
    password_hash = Column(String(60), nullable=False)
    contact = Column(INTEGER, nullable=False)
    about = Column(String)
    location = Column(String, nullable=False)
    products = relationship("Products", backref="business", cascade="all, delete, delete-orphan")

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

from models.base_model import FarmModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Users(FarmModel, Base):
    """class for every user, either registered or not"""
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    # business_name = Column(String(60), nullable=False)
    farm_name = Column(String(60), nullable=False)
    state = Column(String(60), nullable=False)
    products = relationship("Products", backref="users", cascade="all, delete, delete-orphan")

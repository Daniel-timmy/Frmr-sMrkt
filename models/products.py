from models.base_model import FarmModel, Base
from sqlalchemy import Column, ForeignKey, String, INTEGER, BOOLEAN, LargeBinary


class Products(FarmModel, Base):
    """Products class"""
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}

    product_images = Column(LargeBinary)
    price = Column(INTEGER, nullable=False)
    farm_name = Column(String(60), nullable=False)
    product_name = Column(String(60), nullable=False)
    contact = Column(INTEGER, nullable=False)
    logged_users_name = Column(String, ForeignKey('loggedUsers.farm_name'))
    users_name = Column(String, ForeignKey('users.farm_name'))


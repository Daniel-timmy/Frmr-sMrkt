
from models.base_model import FarmModel, Base
from sqlalchemy import Column, String


class Reviews(FarmModel, Base):
    """Products class"""
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}

    product_id = Column(String, nullable=False)
    comment = Column(String)

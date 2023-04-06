"""Basemodel class for other classes"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import storage
import uuid

Base = declarative_base()


class FarmModel:
    """The base model for all classes in models"""
    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())

    def __init__(self):
        """initializes the base model attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()

    def save(self):
        """saves a newly created object or updates an old object"""
        import models
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """deletes an instance from storage"""
        storage.delete(self)

    def to_dict(self):
        """formats object to a dictionary representation"""
        new_dict = self.__dict__.copy()
        if "_sa_instance_state" in new_dict.keys():
            del new_dict['_sa_instance_state']
        return new_dict

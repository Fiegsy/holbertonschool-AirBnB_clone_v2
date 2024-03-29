#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from models import storage  

Base = declarative_base()

class BaseModel(Base):
    """A base class for all hbnb models"""
    __tablename__ = 'base_models'

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls_name = self.__class__.__name__
        return '[{}] ({}) {}'.format(cls_name, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        try:
            self.updated_at = datetime.utcnow()
            storage.new(self)
            storage.save()
        except Exception as e:
            print(f"Error saving instance: {e}")

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """Deletes the current instance from storage"""
        try:
            storage.delete(self)
        except Exception as e:
            print(f"Error deleting instance: {e}")

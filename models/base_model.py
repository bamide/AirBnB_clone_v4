#!/usr/bin/python3
"""A module that defines a BaseModel class"""
import uuid
import models
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()


class BaseModel:
    """A Base class with all public instances"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the class"""
        # Check if kwargs is not empty
        if kwargs:
            # Iterate through the key-value pairs in kwargs
            for key, value in kwargs.items():
                if key != '__class__':
                    if not hasattr(self, key):
                        setattr(self, key, value)
            if 'id' not in kwargs:
                setattr(self, 'id', str(uuid4()))

    def save(self):
        """Update the updated_at attribute to the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__
        of the instance
        """
        new_d = self.__dict__.copy()
        if '_sa_instance_state' in new_d:
            del new_d['_sa_instance_state']
        for key, value in new_d.items():
            if isinstance(value, datetime):
                new_d[key] = value.isoformat()
        return new_d

    def __str__(self):
        """return the string representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def delete(self):
        """deletes instance"""
        models.storage.delete(self)

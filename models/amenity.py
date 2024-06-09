#!/usr/bin/python3
"""Module that defines class Amenity"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Table


class Amenity(BaseModel, Base):
    """Amenity class that inherits from BaseModel"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
            "Place", secondary="place_amenity", back_populates="amenities")

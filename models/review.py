#!/usr/bin/python3
"""Module that defines class Review"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey


class Review(BaseModel, Base):
    """Review class that inherits from BaseModel"""
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

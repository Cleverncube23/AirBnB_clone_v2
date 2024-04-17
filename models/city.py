#!/usr/bin/python3
"""City Module for HBNB project"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class City(BaseModel, Base):
    """The City class, contains state ID and name"""

    if models.is_type == "db":
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='city', cascade='delete')

    else:
        state_id = ""
        name = ""

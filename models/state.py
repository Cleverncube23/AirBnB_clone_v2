#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class State(BaseModel, Base):
    """ State class """

    if models.is_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete-orphan')

    else:
        name = ""

    @property
    def cities(self):
        """ Getter attribute for cities """
        cities_list = []
        if models.is_type == 'db':
            for city in self.cities:
                if city.state_id == self.id:
                    cities_list.append(city)
        else:
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    cities_list.append(city)
        return cities_list

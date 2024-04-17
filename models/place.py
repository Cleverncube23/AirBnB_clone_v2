#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
import models
from models.review import Review
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table

# Define the relationship table for many-to-many between Place and Amenity if using db storage
if models.is_type == "db":
    relationship_table = Table('place_amenity', Base.metadata,
                               Column('place_id', String(60),
                                      ForeignKey('places.id'),
                                      nullable=False),
                               Column('amenity_id', String(60),
                                      ForeignKey('amenities.id'),
                                      nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    # Relationships
    amenities = relationship('Amenity', secondary=relationship_table, viewonly=False)
    
    if models.is_type == "db":
        reviews = relationship('Review', backref='place', cascade='delete')
    else:
        # FileStorage specific properties and methods
        amenity_ids = []

        @property
        def reviews(self):
            """ Getter for reviews when using FileStorage """
            all_reviews = models.storage.all(Review).values()
            return [review for review in all_reviews if review.place_id == self.id]

        @property
        def amenities(self):
            """ Getter for amenities when using FileStorage """
            all_amenities = models.storage.all(Amenity).values()
            return [amenity for amenity in all_amenities if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """ Setter for amenities that appends amenity ids when using FileStorage """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)

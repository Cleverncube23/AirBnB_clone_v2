import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()

class BaseModel(Base):
    """Base class for all models in our hbnb clone"""

    __tablename__ = 'base_model'  # Table name for SQLAlchemy mapping (optional)

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of the instance"""
        cls = type(self).__name__
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Save the current instance to the storage"""
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance"""
        obj_dict = self.__dict__.copy()
        obj_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy state key if present
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict['__class__'] = type(self).__name__
        return obj_dict

#!/usr/bin/python3
"""
This module defines a DBStorage class to manage database storage
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv


class DBStorage:
    """A class to manage database storage"""

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes DBStorage with a database engine
        """
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries objects from the database based on class name
        """
        from models import classes

        objects = {}

        if cls:
            query = self.__session.query(classes[cls])
            for obj in query.all():
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for cls in classes.values():
                query = self.__session.query(cls)
                for obj in query.all():
                    key = '{}.{}'.format(type(obj).__name__, obj.id)
                    objects[key] = obj

        return objects

    def new(self, obj):
        """
        Adds a new object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and initializes session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Closes the current session
        """
        self.__session.close()

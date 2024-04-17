#!/usr/bin/python3
"""
This module initializes the appropriate storage based on environment variables
"""

from os import getenv

is_type = getenv("HBNB_TYPE_STORAGE")

if is_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()

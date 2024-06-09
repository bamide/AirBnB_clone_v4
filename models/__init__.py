#!/usr/bin/python3
"""init"""
from models.engine.file_storage import FileStorage
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE', 'file')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()

#!/usr/bin/python3
"""This module instantiates a storage object based on the storage type"""

from os import getenv

from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

storage_type = getenv("HBNB_TYPE_STORAGE", "file")

if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()

#!/usr/bin/python3
"""
Module: __init__.py

This module initializes the FileStorage instance for
the AirBnB_clone project.

It imports the FileStorage class from the models.engine.
file_storage module and creates
an instance named 'storage'. It then calls the 'reload'
method to load previously stored
data into the storage.

Usage:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()
    storage.reload()
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()

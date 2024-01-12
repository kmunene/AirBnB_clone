#!/usr/bin/python3
"""
Module: __init__.py

This module initializes the FileStorage instance for the
AirBnB_clone project.

"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()

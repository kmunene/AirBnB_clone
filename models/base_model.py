#!/usr/bin/python3
"""
BaseModel Class that defines all common
    attributes/methods for other classes
"""


import uuid
from datetime import datetime
from os.path import exists
import models


class BaseModel:
    """
    Base class for other classes in the project,
    providing common attributes
    and methods for data models.

    Attributes:
        id (str): Unique identifier for the
        instance (generated using UUID).
        created_at (datetime): Timestamp
        indicating the creation time of the instance.
        updated_at (datetime): Timestamp
        indicating the last update time of the instance.

    Methods:
        __init__(*args, **kwargs): Constructor
        method, initializes instance attributes.
        __str__(): String representation of the
        instance.
        save(): Updates the 'updated_at'
        attribute and saves the instance to storage.
        to_dict(): Converts the instance to
        a dictionary for serialization.

    Usage:
        To create a new data model class, inherit
        from this BaseModel and
        implement class-specific attributes and
        methods.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor method for BaseModel.

        Parameters:
            args: Variable length argument list.
            kwargs: Variable length keyword
            argument list.

        Notes:
            If keyword arguments are provided,
            the method sets instance attributes
            based on the provided values. If not,
            it generates a new UUID for 'id'
            and sets 'created_at' and 'updated_at'
            timestamps before saving the instance.
        """
        if kwargs:
            date_format = '%Y-%m-%dT%H:%M:%S.%f'
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.strptime(value, date_format)
                    setattr(self, key, value)
            models.storage.new(self)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        String representation of the BaseModel instance.

        Returns:
            str: A string containing the class name,
            instance ID, and attribute dictionary.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Update the 'updated_at' attribute and save
        the instance to storage.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Convert the instance to a dictionary for serialization.

        Returns:
            dict: A dictionary containing the instance attributes.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

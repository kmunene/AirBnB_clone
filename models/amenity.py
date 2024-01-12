#!/usr/bin/python3
"""
Module containing the Amenity class, a subclass of BaseModel.
"""

from models.base_model import BaseModel

class Amenity(BaseModel):
    """
    Amenity class represents an amenity that can be
    associated with a place in the AirBnB application.

    Attributes:
        name (str): The name of the amenity.
    """

    name = ""

#!/usr/bin/python3
"""
Module containing the City class, a subclass of BaseModel.
"""

from models.base_model import BaseModel

class City(BaseModel):
    """
    City class represents a city in the AirBnB application.

    Attributes:
        state_id (str): The ID of the state to which the city belongs.
        name (str): The name of the city.
    """

    state_id = ""
    name = ""

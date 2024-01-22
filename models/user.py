#!/usr/bin/python3
"""
Module containing the User class, a subclass of BaseModel.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    User class represents a user in the AirBnB application.

    Attributes:
        email (str): The email address of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

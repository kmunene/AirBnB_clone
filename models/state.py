#!/usr/bin/python3
"""
Module containing the State class, a subclass of BaseModel.
"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    State class represents a state in the AirBnB application.

    Attributes:
        name (str): The name of the state.
    """

    name = ""

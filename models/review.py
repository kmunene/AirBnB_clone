#!/usr/bin/python3
"""
Module containing the Review class, a subclass of BaseModel.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class represents a review for a place in the AirBnB application.

    Attributes:
        place_id (str): The ID of the place for which the review is written.
        user_id (str): The ID of the user who wrote the review.
        text (str): The text content of the review.
    """

    place_id = ""
    user_id = ""
    text = ""

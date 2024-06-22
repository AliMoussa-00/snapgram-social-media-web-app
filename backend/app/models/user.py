#!/usr/bin/env python3
""" Defining the User module """

from typing import Optional
from pydantic import EmailStr
from app.models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user in the application.

    Attributes:
        email (EmailStr): Email address of the user.
        hashed_password (str): Hashed password for user authentication.
        username (str): Unique username for the user.
        full_name (Optional[str], optional): Full name of the user.
        bio (Optional[str], optional): Biography or profile description of the user.
        profile_picture_url (Optional[str], optional): URL or path to the user's profile picture.

    Settings:
        collection (str): MongoDB collection name for storing User documents.
    """

    email: EmailStr
    hashed_password: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None

    class Settings:
        """
        Settings for the User class.

        Attributes:
            collection (str): Name of the MongoDB collection where User documents are stored.
        """
        name = 'users'

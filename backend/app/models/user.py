#!/usr/bin/env python3
""" Defining the User module """

from beanie import Link
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from app.models.common import Common
from datetime import datetime


class User(Common):
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
        name (str): MongoDB collection name for storing User documents.
    """

    email: EmailStr
    hashed_password: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    followers: Optional[List[Link["User"]]] = []
    following: Optional[List[Link["User"]]] = []

    class Settings:
        """
        Settings for the User class.

        Attributes:
            name (str): Name of the MongoDB collection where User documents are stored.
        """
        name = 'users'


class UserCreateRequest(BaseModel):
    """
    User creation request model for POST requests.

    Attributes:
    - email: The user's email address.
    - password: The user's password (to be hashed before storing).
    - username: The user's username.
    - full_name: The user's full name (optional).
    - bio: A short biography of the user (optional).
    - profile_picture_url: URL to the user's profile picture (optional).
    """
    email: EmailStr
    password: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UpdateUserRequest(BaseModel):
    """
    User update request model for PUT requests.

    Attributes:
    - email: The user's email address (optional).
    - password: The user's password (optional, to be hashed before storing).
    - username: The user's username (optional).
    - full_name: The user's full name (optional).
    - bio: A short biography of the user (optional).
    - profile_picture_url: URL to the user's profile picture (optional).
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserResponse(BaseModel):
    """
    User response model for API responses.

    Attributes:
    - id: The user's ID.
    - email: The user's email address.
    - username: The user's username.
    - full_name: The user's full name (optional).
    - created_at: The timestamp when the user was created (optional).
    - updated_at: The timestamp when the user was last updated (optional).
    - bio: A short biography of the user (optional).
    - profile_picture_url: URL to the user's profile picture (optional).
    """
    id: Optional[str] = Field(alias="_id")
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        str_strip_whitespace = True
        json_encoders = {
            datetime: lambda date: date.isoformat(),
        }

#!/usr/bin/env python3
""" Defining the Post module """

from app.models.common import Common
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Post(Common):
    """
    Represents a user in the application.

    Attributes:
        user_id (str): Unique user_id for the user.
        content (str): content of the post.
        media_type (str): type media of the post.
        media_url (str): URL of the post.

    Settings:
        name (str): MongoDB collection name for storing Post documents.
    """
    user_id: str
    content: str
    media_type: str
    media_url: str

    class Settings:
        """
        Settings for the Post class .
        Attributes:
            name(str): Name of the MongoDB collection
            where Post documents are stored.
        """
        name = 'posts'


class PostCreateRequest(BaseModel):
    """
    Post creation request model for POST requests.

    Attributes:
        user_id (str): The ID of the user who created the post.
        content (str): The content of the post.
        media_type (str): The type of media associated with the post (e.g., image, video).
        media_url (str): The URL of the media associated with the post.
    """
    user_id: str
    content: str
    media_type: str
    media_url: str


class UpdatePostRequest(BaseModel):
    """
    Post update request model for PUT requests.

    Attributes:
        content (Optional[str], optional): The content of the post.
        media_type (Optional[str], optional): The type of media associated with the post (e.g., image, video).
        media_url (Optional[str], optional): The URL of the media associated with the post.
    """
    content: Optional[str] = None
    media_type: Optional[str] = None
    media_url: Optional[str] = None


class PostResponse(BaseModel):
    """
    Post response model for API responses.

    Attributes:
        id (str): The ID of the post.
        user_id (str): The ID of the user who created the post.
        content (str): The content of the post.
        media_type (str): The type of media associated with the post (e.g., image, video).
        media_url (str): The URL of the media associated with the post.
        created_at (datetime): The timestamp when the post was created.
        updated_at (datetime): The timestamp when the post was last updated.
    """
    id: Optional[str] = Field(alias="_id")
    user_id: str
    content: str
    media_type: str
    media_url: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        populate_by_name = True
        str_strip_whitespace = True
        json_encoders = {
            datetime: lambda date: date.isoformat(),
        }

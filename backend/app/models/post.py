#!/usr/bin/env python3
""" Defining the Post module """

from app.models.common import Common


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

#!/usr/bin/env python3
""" Defining the Post module """

from app.models.common import Common
from app.models.comment import Comment
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime
from beanie import Link


class Post(Common):
    """
    Represents a user in the application.

    Attributes:
        user_id (str): ID of the user who created the post.
        content (Optional[str]): Text content of the post.
        media_type (Optional[str]): Type of media (e.g., image, video).
        media_url (Optional[str]): URL or path to the media associated with the post.

    Settings:
        name (str): MongoDB collection name for storing Post documents.
    """
    user_id: str
    content: Optional[str] = None
    media_type: Optional[str] = None
    media_url: Optional[str] = None
    comments: Optional[List[Link[Comment]]] = []

    class Settings:
        """
        Settings for the Post class .
        Attributes:
            name(str): Name of the MongoDB collection
            where Post documents are stored.
        """
        name = 'posts'

    async def add_comment(self, comment: Comment):
        self.comments.append(comment)
        await self.save()

    async def remove_comment(self, comment: Comment):
        self.comments = [cmt for cmt in self.comments if cmt.id != comment.id]
        await self.save()

    @model_validator(mode='before')
    def check_content_or_media_url(cls, values):
        content = values.get('content')
        media_type = values.get('media_type')
        if not content and not media_type:
            raise ValueError('Either content or media_url must be present')
        return values


class PostCreateRequest(BaseModel):
    """
    Post creation request model for POST requests.

    Attributes:
         user_id (str): ID of the user creating the post.
        content (Optional[str]): Text content of the post.
        media_type (Optional[str]): Type of media (e.g., image, video).
        media_url (Optional[str]): URL or path to the media associated with the post.
    """
    user_id: str
    content: Optional[str] = None
    media_type: Optional[str] = None
    media_url: Optional[str] = None

    @model_validator(mode='before')
    def check_content_or_media_url(cls, values):
        content = values.get('content')
        media_type = values.get('media_type')
        if not content and not media_type:
            raise ValueError('Either content or media_url must be present')
        return values


class UpdatePostRequest(BaseModel):
    """
    Post update request model for PUT requests.

    Attributes:
        content (Optional[str]): Updated text content of the post.
        media_type (Optional[str]): Updated type of media (e.g., image, video).
        media_url (Optional[str]): Updated URL or path to the media associated with the post.
    """
    content: Optional[str] = None
    media_type: Optional[str] = None
    media_url: Optional[str] = None

    @model_validator(mode='before')
    def check_content_or_media_url(cls, values):
        content = values.get('content')
        media_url = values.get('media_url')
        if not content and not media_url:
            raise ValueError('Either content or media_url must be present')
        return values


class PostResponse(BaseModel):
    """
    Post response model for API responses.

    Attributes:
        id (Optional[str]): Unique identifier for the post
        user_id (str): ID of the user who created the post.
        content (Optional[str]): Text content of the post.
        media_type (Optional[str]): Type of media (e.g., image, video).
        media_url (Optional[str]): URL or path to the media associated with the post.
        created_at (Optional[datetime]): Timestamp when the post was created.
        updated_at (Optional[datetime]): Timestamp when the post was last updated.
    """
    id: Optional[str] = Field(alias="_id")
    user_id: str
    content: Optional[str] = None
    media_type: Optional[str] = None
    media_url: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        populate_by_name = True
        str_strip_whitespace = True
        json_encoders = {
            datetime: lambda date: date.isoformat(),
        }

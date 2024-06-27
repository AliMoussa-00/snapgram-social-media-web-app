#!/usr/bin/env python3
""" Defining the Comment module """

from typing import Optional
from app.models.common import Common
from pydantic import BaseModel, Field
from datetime import datetime


class Comment(Common):
    """
    Represents a comment in the application.

    Attributes:
        post_id (str): ID of the post being commented on.
        user_id (str): ID of the user who made the comment.
        content (str): Text content of the comment.
    Settings:
        name (str): MongoDB collection name for storing Comment documents.
    """

    post_id: str
    user_id: str
    content: str

    class Settings:
        """
        Settings for the Comment class.

        Attributes:
            name (str): Name of the MongoDB collection where Comment documents are stored.
        """
        name = 'comments'


class CommentCreateRequest(BaseModel):
    """
    Comment creation request model for POST requests.

    Attributes:
        post_id (str): ID of the post being commented on.
        user_id (str): ID of the user making the comment.
        content (str): Text content of the comment.
    """
    post_id: str
    user_id: str
    content: str


class UpdateCommentRequest(BaseModel):
    """
    Comment update request model for PUT requests.

    Attributes:
        content (Optional[str]): Text content of the comment.
    """
    content: Optional[str] = None


class CommentResponse(BaseModel):
    """
    Comment response model for API responses.

    Attributes:
        id (Optional[str]): Unique identifier for the comment.
        post_id (str): ID of the post being commented on.
        user_id (str): ID of the user who made the comment.
        content (str): Text content of the comment.
        created_at (Optional[datetime]): Timestamp when the comment was created.
        updated_at (Optional[datetime]): Timestamp when the comment was last updated.
    """
    id: Optional[str] = Field(alias="_id")
    post_id: str
    user_id: str
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        populate_by_name = True
        str_strip_whitespace = True
        json_encoders = {
            datetime: lambda date: date.isoformat(),
        }

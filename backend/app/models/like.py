#!/usr/bin/env python3
""" Defining the Like module """

from pydantic import BaseModel, Field
from app.models.common import Common
from typing import Optional
from datetime import datetime


class Like(Common):
    """
    Represents a like in the application.

    Attributes:
        user_id (str): ID of the user who gave the like.
        post_id (Optional[str]): ID of the post that was liked.
    """
    user_id: str
    post_id: str

    class Settings:
        """
        Settings for the Post class .
        Attributes:
            name(str): Name of the MongoDB collection
            where Like documents are stored.
        """
        name = 'likes'


class LikeCreateRequest(BaseModel):
    """Request model for creating a like."""
    user_id: str
    post_id: str


class LikeResponse(BaseModel):
    """
    Response model for representing a like.

    Attributes:
        id (Optional[str]): ID of the like document.
        user_id (str): ID of the user who gave the like.
        post_id (str): ID of the post that was liked.
        created_at (Optional[datetime]): Timestamp for when the like was created.
        updated_at (Optional[datetime]): Timestamp for when the like was last updated.
    """
    id: Optional[str] = Field(alias="_id")
    user_id: str
    post_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        populate_by_name = True
        str_strip_whitespace = True
        json_encoders = {
            datetime: lambda date: date.isoformat(),
        }

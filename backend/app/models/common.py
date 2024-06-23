#!/usr/bin/env python3
"""
The BaseModel module that all classes will inherit from
"""

from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime
import uuid


class Common(Document):
    """
    Base class for MongoDB documents using Beanie and Pydantic.

    Attributes:
        id (Optional[str]): Unique identifier for the document.
        created_at (Optional[datetime]): Timestamp for document creation.
        updated_at (Optional[datetime]): Timestamp for document update.
    """

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), alias='_id')
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        """
        Pydantic configuration settings for BaseModel.

        Configures:
            - orm_mode: Enable Pydantic's ORM mode for MongoDB document interaction.
            - anystr_strip_whitespace: Strip whitespace from string fields.
            - json_encoders: Custom JSON encoder for datetime objects.
        """
        from_attributes = True
        str_strip_whitespace = True
        json_encoders = {
            datetime: lambda date: date.isoformat(),
        }

    def update_timestamps(self) -> None:
        """
        Update the `updated_at` timestamp to the current datetime.
        """
        self.updated_at = datetime.now()

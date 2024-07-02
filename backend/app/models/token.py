#!/usr/bin/env python3
"""token module"""

from typing import Optional
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Represents a token pair for authentication.

    Attributes:
        access_token (str): The access token used for authenticating requests.
        refresh_token (str): The refresh token used for obtaining a new access token.
        token_type (Optional[str]): The type of token, default is 'bearer'.
    """
    access_token: str
    refresh_token: str
    token_type: Optional[str] = 'Bearer'


class BlackListedTokens(Document):
    """
    Represents a blacklisted token, which will be used in logout.

    Attributes:
        token (str): The blacklisted token.
        black_listed_on (datetime): The date and time when the token was blacklisted.
    """
    token: str
    black_listed_on: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "black_listed_tokens"

    @classmethod
    async def is_token_blacklisted(cls, token: str) -> bool:
        """
        Checks if a token is blacklisted.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is blacklisted, False otherwise.
        """

        black_listed_token = await cls.find_one({"token": token})
        return black_listed_token is not None

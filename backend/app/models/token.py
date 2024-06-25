#!/usr/bin/env python3
"""token module"""

from typing import Optional
from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Optional[str] = 'bearer'


class BlackListedTokens(Document):
    token: str
    black_listed_on: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "black_listed_tokens"

    @classmethod
    async def is_token_blacklisted(cls, token: str) -> bool:
        black_listed_token = await cls.find_one({"token": token})

        return black_listed_token is not None

#!/usr/bin/env python3
""" Module for MongoDB database connection. """
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import CONFIG
from app.models.post import Post
from app.models.user import User
from app.models.token import BlackListedTokens
from app.models.comment import Comment
from app.models.like import Like


async def init_db():
    """
    Initialize MongoDB database connection and setup Beanie ORM.
    This function connects to MongoDB using the MONGODB_URL.
    Note: Beanie is an async MongoDB ORM for Python.
    """
    try:
        client = AsyncIOMotorClient(CONFIG.mongodb_url)
        database = client[CONFIG.db_name]
        await init_beanie(database, document_models=[User, Post, Comment, Like, BlackListedTokens])
    except Exception as e:
        raise ConnectionError(f"Failed to connect to the database: {e}")

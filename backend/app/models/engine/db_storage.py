#!/usr/bin/env python3
""" Module for MongoDB database connection. """
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGODB_URL, DB_NAME
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment


async def init_db():
    """
    Initialize MongoDB database connection and setup Beanie ORM.
    This function connects to MongoDB using the MONGODB_URL.
    Note: Beanie is an async MongoDB ORM for Python.
    """
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client[DB_NAME]
        await init_beanie(database, document_models=[User, Post, Comment])
        print("Database connection established successfully.")
    except Exception as e:
        raise ConnectionError(f"Failed to connect to the database: {e}")

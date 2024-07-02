#!/usr/bin/env python3
""" testing the posts endpoints """

import uuid
import pytest
from httpx import AsyncClient
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.comment import Comment
from app.models.post import Post
from app.models.token import BlackListedTokens
from app.models.user import User
from app.models.like import Like
from app.api.app import app


@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[User, Post, Comment, Like, BlackListedTokens])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.mark.anyio
async def test_like_post_success():
    """Test liking a post successfully."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user and obtain tokens
        unique_id = uuid.uuid4()
        unique_email = f"test_delete_{unique_id}@example.com"
        unique_username = f"test_delete_{unique_id}"
        register_data = {
            "email": unique_email,
            "username": unique_username,
            "password": "testpassword"
        }
        login_response = await ac.post("/auth/register", json=register_data)
        assert login_response.status_code == 201
        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Fetch the user to get the correct ID
        user_response = await ac.get("/auth/me", headers=headers)
        assert user_response.status_code == 200
        user_id = user_response.json()['_id']

        # Create a post for the user
        post_data = {
            "user_id": user_id,
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/image.jpg"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        post_id = post_response.json()["_id"]

        # Like the post
        like_data = {
            "user_id": user_id,
            "post_id": post_id
        }
        response = await ac.post("/likes/", json=like_data, headers=headers)
        assert response.status_code == 201
        like_response = response.json()
        assert like_response["user_id"] == like_data["user_id"]
        assert like_response["post_id"] == like_data["post_id"]


@pytest.mark.anyio
async def test_get_all_likes_of_post():
    """Test the retrieval of all likes of a post."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user and obtain tokens
        unique_id = uuid.uuid4()
        unique_email = f"test_delete_{unique_id}@example.com"
        unique_username = f"test_delete_{unique_id}"
        register_data = {
            "email": unique_email,
            "username": unique_username,
            "password": "testpassword"
        }
        login_response = await ac.post("/auth/register", json=register_data)
        assert login_response.status_code == 201
        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Fetch the user to get the correct ID
        user_response = await ac.get("/auth/me", headers=headers)
        assert user_response.status_code == 200
        user_id = user_response.json()['_id']

        # Create a post for the user
        post_data = {
            "user_id": user_id,
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/image.jpg"
        }
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        post_id = post_response.json()["_id"]

        # Like the post
        like_data = {
            "user_id": user_id,
            "post_id": post_id
        }
        await ac.post("/likes/", json=like_data, headers=headers)

        # Retrieve all likes of the post
        response = await ac.get(f"/likes/post/{post_id}", headers=headers)
        assert response.status_code == 200

        likes_response = response.json()
        assert isinstance(likes_response, list)
        assert len(likes_response) == 1

        like_resp = likes_response[0]
        assert like_resp["user_id"] == like_data["user_id"]
        assert like_resp["post_id"] == like_data["post_id"]


@pytest.mark.anyio
async def test_unlike_post():
    """Test unliking a post successfully."""

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user and obtain tokens
        unique_id = uuid.uuid4()
        unique_email = f"test_delete_{unique_id}@example.com"
        unique_username = f"test_delete_{unique_id}"
        register_data = {
            "email": unique_email,
            "username": unique_username,
            "password": "testpassword"
        }
        login_response = await ac.post("/auth/register", json=register_data)
        assert login_response.status_code == 201
        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Fetch the user to get the correct ID
        user_response = await ac.get("/auth/me", headers=headers)
        assert user_response.status_code == 200
        user_id = user_response.json()['_id']

        # Create a post for the user
        post_data = {
            "user_id": user_id,
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/image.jpg"
        }
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        post_id = post_response.json()["_id"]

        # Like the post
        like_data = {
            "user_id": user_id,
            "post_id": post_id
        }
        like_response = await ac.post("/likes/", json=like_data, headers=headers)
        assert like_response.status_code == 201
        like_id = like_response.json()["_id"]

        # Unlike the post
        response = await ac.delete(f"/likes/{like_id}", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Like deleted successfully"}

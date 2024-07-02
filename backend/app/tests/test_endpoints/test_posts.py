#!/usr/bin/env python3
"""Testing the posts endpoints"""

import uuid
import pytest
from httpx import AsyncClient
from app.api.app import app
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.token import BlackListedTokens
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[User, Post, Comment, Like, BlackListedTokens])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.mark.anyio
async def test_create_post():
    """Test creating a post."""
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

        # Create a new post with valid token
        post_data = {
            "user_id": user_id,
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/image.jpg"
        }
        response = await ac.post("/posts/", json=post_data, headers=headers)
        assert response.status_code == 201

        post_response = response.json()
        assert post_response["content"] == "This is a test post."
        assert post_response["media_type"] == "image"
        assert post_response["media_url"] == "http://example.com/image.jpg"


@pytest.mark.anyio
async def test_get_all_posts():
    """Test retrieving all posts."""
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

        # Send a GET request to retrieve all posts with valid token
        response = await ac.get("/posts/", headers=headers)
        assert response.status_code == 200

        posts_response = response.json()
        assert isinstance(posts_response, list)


@pytest.mark.anyio
async def test_get_post_by_id():
    """Test retrieving a single post by ID."""
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
            "media_url": "http://example.com/user_image.jpg"
        }
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        post_id = post_response.json()["_id"]

        # Send a GET request to retrieve the post with valid token
        response = await ac.get(f"/posts/{post_id}", headers=headers)
        assert response.status_code == 200

        post_response = response.json()
        assert post_response["content"] == "This is a test post."
        assert post_response["media_type"] == "image"
        assert post_response["media_url"] == "http://example.com/user_image.jpg"


@pytest.mark.anyio
async def test_get_all_posts_of_user():
    """Test retrieving all posts of a user."""

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
            "content": "This is a test post for the user.",
            "media_type": "image",
            "media_url": "http://example.com/user_image.jpg"
        }
        await ac.post("/posts/", json=post_data, headers=headers)

        # Send a GET request to retrieve all posts of the user with valid token
        response = await ac.get(f"/posts/user/{user_id}", headers=headers)
        assert response.status_code == 200

        posts_response = response.json()
        assert isinstance(posts_response, list)
        assert len(posts_response) > 0


@pytest.mark.anyio
async def test_delete_post_by_id():
    """Test deleting a post by ID."""
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
            "media_url": "http://example.com/user_image.jpg"
        }
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        post_id = post_response.json()["_id"]

        comment_data = {
            "post_id": post_id,
            "user_id": user_id,
            "content": "New comment content"
        }
        response = await ac.post("/comments/", json=comment_data, headers=headers)
        assert response.status_code == 201

        # Send a DELETE request to delete the post with valid token
        response = await ac.delete(f"/posts/{post_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Post deleted successfully"

        # Ensure the post no longer exists
        response = await ac.get(f"/posts/{post_id}", headers=headers)
        assert response.status_code == 404

        get_comment_response = await ac.get(f"/comments/post/{post_id}", headers=headers)
        assert get_comment_response.status_code == 404


@pytest.mark.anyio
async def test_create_post_with_no_content_and_no_media_url():
    """Test creating a post with neither content nor media_url should fail."""
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

        # Attempt to create a post with neither content nor media_url
        post_data = {
            "user_id": user_id,
        }
        response = await ac.post('/posts/', json=post_data, headers=headers)

        assert response.status_code == 422  # 422 Unprocessable Entity


@pytest.mark.anyio
async def test_update_post_with_no_content_and_no_media_url():
    """Test updating a post with neither content nor media_url should fail."""
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
            "content": "Original content",
            "media_type": "image",
            "media_url": "http://example.com/original.jpg"
        }
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        post_id = post_response.json()['_id']

        # Attempt to update the post with no content and no media_url
        updated_post_data = {}
        response = await ac.put(f"/posts/{post_id}", json=updated_post_data, headers=headers)

        assert response.status_code == 422  # 422 Unprocessable Entity

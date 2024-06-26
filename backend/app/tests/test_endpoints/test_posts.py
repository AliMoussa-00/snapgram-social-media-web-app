#!/usr/bin/env python3
"""Testing the posts endpoints"""

from app.utils.auth import create_access_token
import pytest
from httpx import AsyncClient
from app.api.app import app
from app.models.user import User
from app.models.post import Post
from app.models.token import BlackListedTokens
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[User, Post, BlackListedTokens])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.mark.anyio
async def test_create_post():
    """Test creating a post."""

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user and obtain tokens
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        await ac.post("/auth/register", json=register_data)

        login_data = {
            "username": "test@example.com",
            "password": "testpassword"
        }
        login_response = await ac.post("/auth/login", data=login_data)
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Create a new post with valid token
        post_data = {
            "user_id": "some_user_id",
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/image.jpg"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.post("/posts/", json=post_data, headers=headers)
        assert response.status_code == 201

        post_response = response.json()
        assert post_response["content"] == post_data["content"]
        assert post_response["media_type"] == post_data["media_type"]
        assert post_response["media_url"] == post_data["media_url"]


@pytest.mark.anyio
async def test_get_all_posts():
    """Test retrieving all posts."""

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user and obtain tokens
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        await ac.post("/auth/register", json=register_data)

        login_data = {
            "username": "test@example.com",
            "password": "testpassword"
        }
        login_response = await ac.post("/auth/login", data=login_data)
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Send a GET request to retrieve all posts with valid token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.get("/posts/", headers=headers)
        assert response.status_code == 200

        posts_response = response.json()
        assert isinstance(posts_response, list)
        assert len(posts_response) > 0  # Ensure there is at least one post


@pytest.mark.anyio
async def test_get_post_by_id():
    """Test retrieving a single post by ID."""

    # Create a post to test retrieval
    post = Post(user_id="some_user_id", content="This is a test post by ID.",
                media_type="image", media_url="http://example.com/image.jpg")
    await post.create()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user and obtain tokens
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        await ac.post("/auth/register", json=register_data)

        login_data = {
            "username": "test@example.com",
            "password": "testpassword"
        }
        login_response = await ac.post("/auth/login", data=login_data)
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Send a GET request to retrieve the post with valid token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.get(f"/posts/{post.id}", headers=headers)
        assert response.status_code == 200

        post_response = response.json()
        assert post_response["content"] == post.content
        assert post_response["media_type"] == post.media_type
        assert post_response["media_url"] == post.media_url


@pytest.mark.anyio
async def test_get_all_posts_of_user():
    """Test retrieving all posts of a user."""

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user and obtain tokens
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        await ac.post("/auth/register", json=register_data)
        user = await User.find_one(User.username == "testuser")

        login_data = {
            "username": "test@example.com",
            "password": "testpassword"
        }
        login_response = await ac.post("/auth/login", data=login_data)
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Create a post for the user
        post_data = {
            "user_id": user.id,
            "content": "This is a test post for the user.",
            "media_type": "image",
            "media_url": "http://example.com/user_image.jpg"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        await ac.post("/posts/", json=post_data, headers=headers)

        # Send a GET request to retrieve all posts of the user with valid token
        response = await ac.get(f"/posts/user/{user.id}", headers=headers)
        assert response.status_code == 200

        posts_response = response.json()
        assert isinstance(posts_response, list)
        assert len(posts_response) > 0


@pytest.mark.anyio
async def test_delete_post_by_id():
    """Test deleting a post by ID."""

    # Create a post to test deletion
    post = Post(user_id="some_user_id", content="This is a test post to delete.",
                media_type="image", media_url="http://example.com/delete_image.jpg")
    await post.create()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user and obtain tokens
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        await ac.post("/auth/register", json=register_data)

        login_data = {
            "username": "test@example.com",
            "password": "testpassword"
        }
        login_response = await ac.post("/auth/login", data=login_data)
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Send a DELETE request to delete the post with valid token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.delete(f"/posts/{post.id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Post deleted successfully"

        # Ensure the post no longer exists
        response = await ac.get(f"/posts/{post.id}", headers=headers)
        assert response.status_code == 404

#!/usr/bin/env python3
""" testing the posts endpoints """
import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.token import BlackListedTokens
from app.models.user import User
from app.utils.auth import hash_password
from app.models.post import Post
from app.models.comment import Comment
from app.api.app import app


@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[User, Post, Comment, BlackListedTokens])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.mark.anyio
async def test_create_comment():
    """Test the creation of a comment endpoint."""
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

        # Fetch the user from the database to get the actual user ID
        user = await User.find_one(User.username == "testuser")

        # Create a post for the user
        post_data = {
            "user_id": str(user.id),
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/user_image.jpg"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        created_post = post_response.json()

        # Create a comment for the post
        comment_data = {
            "post_id": created_post["_id"],
            "user_id": str(user.id),
            "content": "New comment content"
        }
        response = await ac.post("/comments/", json=comment_data, headers=headers)
        assert response.status_code == 201
        comment_response = response.json()
        assert comment_response["post_id"] == created_post["_id"]
        assert comment_response["user_id"] == str(user.id)
        assert comment_response["content"] == "New comment content"


@pytest.mark.anyio
async def test_get_all_comments_of_post():
    """Test retrieving all comments for a post."""
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

        # Fetch the user from the database to get the actual user ID
        user = await User.find_one(User.username == "testuser")

        # Create a post for the user
        post_data = {
            "user_id": str(user.id),
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/user_image.jpg"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        created_post = post_response.json()

        # Create a comment for the post
        comment_data = {
            "post_id": created_post["_id"],
            "user_id": str(user.id),
            "content": "New comment content"
        }
        await ac.post("/comments/", json=comment_data, headers=headers)

        # Retrieve all comments for the post
        response = await ac.get(f"/comments/post/{created_post['_id']}", headers=headers)
        assert response.status_code == 200
        comments_response = response.json()

        assert isinstance(comments_response, list)
        assert len(comments_response) == 1

        comment_resp = comments_response[0]
        assert comment_resp["post_id"] == created_post["_id"]
        assert comment_resp["user_id"] == str(user.id)
        assert comment_resp["content"] == "New comment content"


@pytest.mark.anyio
async def test_update_comment():
    """Test updating a comment."""
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

        # Fetch the user from the database to get the actual user ID
        user = await User.find_one(User.username == "testuser")

        # Create a post for the user
        post_data = {
            "user_id": str(user.id),
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/user_image.jpg"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        created_post = post_response.json()

        # Create a comment for the post
        comment_data = {
            "post_id": created_post["_id"],
            "user_id": str(user.id),
            "content": "New comment content"
        }
        comment_response = await ac.post("/comments/", json=comment_data, headers=headers)
        assert comment_response.status_code == 201
        created_comment = comment_response.json()

        # Update the comment
        update_comment_data = {
            "content": "Updated comment content"
        }
        response = await ac.put(f"/comments/{created_comment['_id']}", json=update_comment_data, headers=headers)
        assert response.status_code == 200

        updated_comment_response = response.json()
        assert updated_comment_response["content"] == "Updated comment content"
        assert updated_comment_response["post_id"] == created_comment["post_id"]
        assert updated_comment_response["user_id"] == created_comment["user_id"]


@pytest.mark.anyio
async def test_delete_comment():
    """Test deleting a comment."""
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

        # Fetch the user from the database to get the actual user ID
        user = await User.find_one(User.username == "testuser")

        # Create a post for the user
        post_data = {
            "user_id": str(user.id),
            "content": "This is a test post.",
            "media_type": "image",
            "media_url": "http://example.com/user_image.jpg"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        post_response = await ac.post("/posts/", json=post_data, headers=headers)
        assert post_response.status_code == 201
        created_post = post_response.json()

        # Create a comment for the post
        comment_data = {
            "post_id": created_post["_id"],
            "user_id": str(user.id),
            "content": "New comment content"
        }
        comment_response = await ac.post("/comments/", json=comment_data, headers=headers)
        assert comment_response.status_code == 201
        created_comment = comment_response.json()

        # Delete the comment
        response = await ac.delete(f"/comments/{created_comment['_id']}", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Comment deleted successfully"}

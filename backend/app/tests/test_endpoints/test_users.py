#!/usr/bin/env python3
""" testing the users endpoints """

import uuid
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
import pytest
from httpx import AsyncClient
from app.api.app import app
from app.models.user import User
from app.models.token import BlackListedTokens
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


# 'fixture': This decorator is used to create a fixture in pytest.
# Fixtures are functions that provide a fixed baseline so that tests can be run reliably and repeatedly.

# The "module" scope means the fixture will be set up once per module.
# All tests in the module will share the same fixture setup and teardown.

# The yield statement pauses the function, handing control back to the test functions that depend on this fixture.
# After the tests run, control returns to this function to execute the teardown code.

@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient(
        "mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[User, Post, Comment, Like, BlackListedTokens])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.mark.anyio
async def test_get_all_users():
    """Test retrieving all users."""
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

        # Send a GET request to retrieve all users with valid token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.get("/users/", headers=headers)

        assert response.status_code == 200

        users_response = response.json()
        assert isinstance(users_response, list)
        assert len(users_response) > 0  # Ensure there is at least one user


@pytest.mark.anyio
async def test_get_user():
    """Test retrieving a single user by ID."""
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

        # Send a GET request to retrieve the user with valid token
        response = await ac.get(f"/users/{user_id}", headers=headers)

        assert response.status_code == 200

        user_response = response.json()
        assert user_response["username"] == unique_username
        assert user_response["email"] == unique_email


@pytest.mark.anyio
async def test_update_user():
    """Test updating a user."""
    updated_user_data = {
        "username": "updateduser",
        "email": "updated@example.com"
    }
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

        # Send a PUT request to update the user with valid token
        response = await ac.put(f"/users/{user_id}", json=updated_user_data, headers=headers)

        assert response.status_code == 200

        user_response = response.json()
        assert user_response["username"] == "updateduser"
        assert user_response["email"] == "updated@example.com"


@pytest.mark.anyio
async def test_delete_user():
    """Test deleting a user."""
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

        # Send a DELETE request to delete the user with valid token
        response = await ac.delete(f"/users/{user_id}", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "user deleted successfully"}

        # Verify the user, posts, and comments are deleted
        get_user_response = await ac.get(f"/users/{user_id}", headers=headers)
        assert get_user_response.status_code == 404

        get_post_response = await ac.get(f"/posts/{post_id}", headers=headers)
        assert get_post_response.status_code == 404

        get_comment_response = await ac.get(f"/comments/post/{post_id}", headers=headers)
        assert get_comment_response.status_code == 404


@pytest.mark.anyio
async def test_follow_user():
    """Test following a user."""
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

        # Follow user2 using user1's access token
        follow_response = await ac.post(f"/users/follow/{user_id}", headers=headers)
        assert follow_response.status_code == 200
        assert follow_response.json() == {"message": "follow successfully"}


@pytest.mark.anyio
async def test_unfollow_user():
    """Test unfollowing a user."""
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

        # Follow user using user1's access token
        follow_response = await ac.post(f"/users/follow/{user_id}", headers=headers)
        assert follow_response.status_code == 200

        # Unfollow user using user1's access token
        unfollow_response = await ac.delete(f"/users/unfollow/{user_id}", headers=headers)
        assert unfollow_response.status_code == 200
        assert unfollow_response.json()["message"] == "Unfollowed successfully"


@pytest.mark.anyio
async def test_get_followers():
    """Test retrieving followers of a user."""
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

        # Send a GET request to retrieve followers
        response = await ac.get(f"/users/{user_id}/followers", headers=headers)

        assert response.status_code == 200
        followers_response = response.json()
        assert isinstance(followers_response, list)


@pytest.mark.anyio
async def test_get_following():
    """Test retrieving users a user is following."""
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

        # Send a GET request to retrieve following users
        response = await ac.get(f"/users/{user_id}/following", headers=headers)

        assert response.status_code == 200
        following_response = response.json()
        assert isinstance(following_response, list)

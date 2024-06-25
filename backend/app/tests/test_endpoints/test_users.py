#!/usr/bin/env python3
""" testing the users endpoints """

from app.utils.auth import create_access_token
import pytest
from httpx import AsyncClient
from app.api.app import app
from app.models.user import User
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
    await init_beanie(database=client.test_db, document_models=[User])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.mark.anyio
async def test_get_all_users():
    """Test retrieving all users."""

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

    # Create a user to test retrieval
    user = User(email="test2@example.com",
                hashed_password="hashedpassword", username="testuser2")
    await user.create()

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

        # Send a GET request to retrieve the user with valid token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.get(f"/users/{user.id}", headers=headers)

        assert response.status_code == 200

        user_response = response.json()
        assert user_response["username"] == "testuser2"
        assert user_response["email"] == "test2@example.com"


@pytest.mark.anyio
async def test_update_user():
    """Test updating a user."""

    # Create a user to test update
    user = User(email="test3@example.com",
                hashed_password="hashedpassword", username="testuser3")
    await user.create()

    updated_user_data = {
        "username": "updateduser",
        "email": "updated@example.com"
    }

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

        # Send a PUT request to update the user with valid token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.put(f"/users/{user.id}", json=updated_user_data, headers=headers)

        assert response.status_code == 200

        user_response = response.json()
        assert user_response["username"] == "updateduser"
        assert user_response["email"] == "updated@example.com"


@pytest.mark.anyio
async def test_delete_user():
    """Test deleting a user."""

    # Create a user to test deletion
    user = User(email="test4@example.com",
                hashed_password="hashedpassword", username="testuser4")
    await user.create()

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

        # Send a DELETE request to delete the user with valid token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.delete(f"/users/{user.id}", headers=headers)

        assert response.status_code == 204

        # Ensure the user no longer exists
        response = await ac.get(f"/users/{user.id}", headers=headers)
        assert response.status_code == 404

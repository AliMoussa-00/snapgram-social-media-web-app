# test_authentication.py

from datetime import datetime, timedelta, timezone
import jwt
import pytest
from httpx import AsyncClient
from app.api.app import app
from app.core.config import CONFIG
from app.models.token import BlackListedTokens
from app.models.user import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[User, BlackListedTokens])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.mark.anyio
async def test_register_and_login():
    # Check if user already exists with the same email or username
    existing_user = await User.find_one({"$or": [{"email": "test@example.com"}, {"username": "testuser"}]})
    if existing_user:
        # Clean up or skip the test if user already exists
        await existing_user.delete()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        response = await ac.post("/auth/register", json=register_data)
        assert response.status_code == 201
        token_response = response.json()
        assert "access_token" in token_response
        assert "refresh_token" in token_response

        # Login with the registered user
        login_data = {
            "username": "test@example.com",  # Using email for login
            "password": "testpassword"
        }
        response = await ac.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token_response = response.json()
        assert "access_token" in token_response
        assert "refresh_token" in token_response


@pytest.mark.anyio
async def test_get_current_user():
    # Check if user already exists with the same email or username
    existing_user = await User.find_one({"$or": [{"email": "test@example.com"}, {"username": "testuser"}]})
    if existing_user:
        # Clean up or skip the test if user already exists
        await existing_user.delete()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register a new user
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        response = await ac.post("/auth/register", json=register_data)
        assert response.status_code == 201

        # Login with the registered user
        login_data = {
            "username": "test@example.com",  # Using email for login
            "password": "testpassword"
        }
        response = await ac.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token_response = response.json()
        access_token = token_response["access_token"]

        # Retrieve current authenticated user
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.get("/auth/me", headers=headers)
        assert response.status_code == 200
        user_response = response.json()
        assert user_response["email"] == "test@example.com"
        assert user_response["username"] == "testuser"


@pytest.mark.anyio
async def test_logout_user():
    """Test logging out a user."""
    existing_user = await User.find_one({"$or": [{"email": "test@example.com"}, {"username": "testuser"}]})
    if existing_user:
        # Clean up or skip the test if user already exists
        await existing_user.delete()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        response = await ac.post("/auth/register", json=register_data)
        assert response.status_code == 201

        login_data = {
            "username": "test@example.com",  # Using email for login
            "password": "testpassword"
        }
        response = await ac.post("/auth/login", data=login_data)
        assert response.status_code == 200
        token_response = response.json()
        access_token = token_response["access_token"]

        # Logout the user
        response = await ac.post("/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"

        # Verify the token is blacklisted
        blacklisted_token = await BlackListedTokens.find_one({"token": access_token})
        assert blacklisted_token is not None

        # Try to use the blacklisted token to access a protected route
        response = await ac.get("/users/", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 401


# #####################
# testing refresh token
@pytest.mark.anyio
async def test_refresh_token_success():
    register_data = {
        "email": "test_refresh_token@example.com",
        "username": "test_refresh_token_user",
        "hashed_password": "hashed_password"
    }
    user = User(**register_data)
    await user.create()

    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    refresh_token = jwt.encode(
        payload, CONFIG.jwt_refresh_secret_key, algorithm="HS256")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/refresh-token", json={"refresh_token": refresh_token})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data


@pytest.mark.anyio
async def test_refresh_token_expired():
    register_data = {
        "email": "test_exp_refresh_token@example.com",
        "username": "test_exp_refresh_token_user",
        "hashed_password": "hashed_password"
    }
    user = User(**register_data)
    await user.create()

    payload = {
        "user_id": user.id,
        "email": user.email,
        # expired token
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
    }
    expired_refresh_token = jwt.encode(
        payload, CONFIG.jwt_refresh_secret_key, algorithm="HS256")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/refresh-token", json={"refresh_token": expired_refresh_token})
        assert response.status_code == 401
        assert response.json() == {"detail": "Refresh token expired"}


@pytest.mark.anyio
async def test_refresh_token_invalid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/refresh-token", json={"refresh_token": "invalid_token"})
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid refresh token"}

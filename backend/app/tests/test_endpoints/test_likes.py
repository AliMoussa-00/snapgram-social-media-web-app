#!/usr/bin/env python3
""" testing the posts endpoints """

import pytest
from httpx import AsyncClient
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.models.like import Like
from app.api.app import app
from app.utils.hashing import hash_password


@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[Post, Comment, Like])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.fixture
async def create_user():
    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("password"),
        username="testuser"
    )
    await user.create()
    return user


@pytest.fixture
async def create_post(create_user):
    post = Post(
        user_id=create_user.id,
        content="Test post content",
        media_type="image",
        media_url="http://example.com/image.jpg"
    )
    await post.create()
    return post


@pytest.fixture
async def create_like(create_user, create_post):
    like = Like(
        post_id=create_post.id,
        user_id=create_user.id,
    )
    await like.create()
    return like


@pytest.mark.anyio
async def test_like_post_success(create_user, create_post):
    """Test the like_post endpoint for successful like creation."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a POST request to create a new like
        response = await ac.post("/likes/", json={
            "user_id": create_user.id,
            "post_id": create_post.id
        })

        # Check assertions
        assert response.status_code == 201

        like_response = response.json()
        assert like_response["user_id"] == create_user.id
        assert like_response["post_id"] == create_post.id


@pytest.mark.anyio
async def test_get_all_likes_of_post(create_post):
    """Test the get_all_likes_of_post endpoint."""

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a GET request to retrieve the likes
        response = await ac.get(f"/likes/post/{create_post.id}")

        # Check assertions
        assert response.status_code == 200
        likes_response = response.json()

        assert isinstance(likes_response, list)
        assert len(likes_response) == 0


@pytest.mark.anyio
async def test_unlike_post(create_like):
    """Test deleting a like."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/likes/{create_like.id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Like deleted successfully"}

        # Verify the like is deleted
        response = await ac.get(f"/likes/post/{create_like.post_id}")
        assert response.status_code == 200
        likes_response = response.json()
        assert all(like["id"] !=
                   create_like.id for like in likes_response)

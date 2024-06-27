#!/usr/bin/env python3
""" testing the posts endpoints """

import pytest
from httpx import AsyncClient
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.api.app import app


@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[Post, Comment])
    yield
    # Drop the test database after tests are done
    await client.drop_database("test_db")


@pytest.mark.anyio
async def test_create_post():
    """Test the creation of a post endpoint."""

    # Create a user to test retrieval
    user = User(email="test1@example.com",
                hashed_password="hashedpassword", username="test1")
    await user.create()

    # Define post data for creation
    post_data = {
        "user_id": user.id,
        "content": "text",
        "media_type": "text",
        "media_url": "url"
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a POST request to create a new post
        response = await ac.post("/posts/", json=post_data)

        assert response.status_code == 201

        post_response = response.json()
        assert post_response["user_id"] == user.id
        assert post_response["content"] == "text"


@pytest.mark.anyio
async def test_get_all_posts():
    """Test retrieving all posts."""

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a GET request to retrieve all posts
        response = await ac.get("/posts/")

        assert response.status_code == 200

        post_response = response.json()
        assert isinstance(post_response, list)
        assert len(post_response) >= 0


@pytest.mark.anyio
async def test_get_all_posts_of_user():
    """Test retrieving all posts of user."""
    # Create a user to test retrieval
    user = User(email="test2@example.com",
                hashed_password="hashedpassword", username="test2")
    await user.create()

    post_data1 = {
        "user_id": user.id,
        "content": "First post",
        "media_type": "image",
        "media_url": "http://example.com/image1.jpg"
    }
    post_data2 = {
        "user_id": user.id,
        "content": "Second post",
        "media_type": "video",
        "media_url": "http://example.com/video1.mp4"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a POST request to create a new posts
        await ac.post("/posts/", json=post_data1)
        await ac.post("/posts/", json=post_data2)
        # Retrieve all posts for the user
        response = await ac.get(f"/posts/user/{user.id}")
        assert response.status_code == 200
        posts_response = response.json()
        assert isinstance(posts_response, list)
        assert len(posts_response) == 2
        assert posts_response[0]["user_id"] == user.id
        assert posts_response[1]["user_id"] == user.id


@pytest.mark.anyio
async def test_get_post_by_id():
    """Test retrieving a post by ID."""
    # Create a user to test retrieval
    user = User(email="test3@example.com",
                hashed_password="hashedpassword", username="test3")
    await user.create()

    post_data = {
        "user_id": user.id,
        "content": "This is a test post",
        "media_type": "image",
        "media_url": "http://example.com/image.jpg"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a POST request to create a new post
        post_response = await ac.post("/posts/", json=post_data)

        assert post_response.status_code == 201

        post = post_response.json()
        response = await ac.get(f"/posts/{post['_id']}")

        assert response.status_code == 200

        retrieved_post = response.json()
        assert retrieved_post["user_id"] == user.id
        assert retrieved_post["content"] == "This is a test post"


@pytest.mark.anyio
async def test_update_post():
    """Test updating a post."""
    # Create a user to test retrieval
    user = User(email="test4@example.com",
                hashed_password="hashedpassword", username="test4")
    await user.create()

    post_data = {
        "user_id": user.id,
        "content": "This is a test post",
        "media_type": "image",
        "media_url": "http://example.com/image.jpg"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a POST request to create a new post
        post_response = await ac.post("/posts/", json=post_data)
        post = post_response.json()
        # Update the post
        updated_post_data = {
            "content": "Updated content",
            "media_type": "video",
            "media_url": "http://example.com/updated.mp4"
        }
        response = await ac.put(f"/posts/{post['_id']}", json=updated_post_data)

        assert response.status_code == 200
        updated_post_response = response.json()
        assert updated_post_response["content"] == "Updated content"
        assert updated_post_response["media_type"] == "video"
        assert updated_post_response["media_url"] == "http://example.com/updated.mp4"


@pytest.mark.anyio
async def test_delete_post_by_id():
    """Test deleting a post."""
    user = User(email="test5@example.com",
                hashed_password="hashedpassword", username="test5")
    await user.create()

    post_data = {
        "user_id": str(user.id),
        "content": "This is a test post",
        "media_type": "image",
        "media_url": "http://example.com/image.jpg"
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        post_response = await ac.post("/posts/", json=post_data)

        assert post_response.status_code == 201
        post = post_response.json()
        post_id = post['_id']  # The correct key is '_id'

        cmt_response = await ac.post("/comments/", json={
            "post_id": post_id,
            "user_id": str(user.id),
            "content": "Good Comment"
        })
        assert cmt_response.status_code == 201

        response = await ac.delete(f"/posts/{post_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Post deleted successfully"}

        response = await ac.delete(f"/posts/{post_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Post not found!"


@pytest.mark.anyio
async def test_create_post_with_no_content_and_no_media_url():
    """Test creating a post with neither content nor media_url should fail."""
    # Create a user to test retrieval
    user = User(email="test6@example.com",
                hashed_password="hashedpassword", username="test6")
    await user.create()

    post_data = {
        "user_id": user.id,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a POST request to create a new post
        response = await ac.post('/posts/', json=post_data)

        assert response.status_code == 422


@pytest.mark.anyio
async def test_update_post_with_no_content_and_no_media_url():
    """Test updating a post with neither content nor media_url should fail."""
    user = User(email="test7@example.com",
                hashed_password="hashedpassword", username="test7")
    await user.create()

    post_data = {
        "user_id": user.id,
        "content": "Original content",
        "media_type": "image",
        "media_url": "http://example.com/original.jpg"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a POST request to create a new post
        post_response = await ac.post("/posts/", json=post_data)
        post = post_response.json()
        # Attempt to update the post with no content and no media_url
        updated_post_data = {}
        response = await ac.put(f"/posts/{post['_id']}", json=updated_post_data)

        assert response.status_code == 422  # 422 Unprocessable Entity

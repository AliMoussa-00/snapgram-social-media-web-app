#!/usr/bin/env python3
""" testing the posts endpoints """
import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.utils.hashing import hash_password
from app.models.post import Post
from app.models.comment import Comment
from app.api.app import app


@pytest.fixture(scope="module", autouse=True)
async def initialize_db():
    """Initialize the test database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.test_db, document_models=[Post, Comment])
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
async def create_comment(create_user, create_post):
    comment = Comment(
        post_id=create_post.id,
        user_id=create_user.id,
        content="Test comment content"
    )
    await comment.create()
    return comment


@pytest.mark.anyio
async def test_create_comment(create_user, create_post):
    """Test the creation of a comment endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a POST request to create a new post
        response = await ac.post("/comments/", json={
            "post_id": create_post.id,
            "user_id": create_user.id,
            "content": "New comment content"
        })
        assert response.status_code == 201
        comment_response = response.json()
        assert comment_response["post_id"] == create_post.id
        assert comment_response["user_id"] == create_user.id
        assert comment_response["content"] == "New comment content"


@pytest.mark.anyio
async def test_get_all_comments():
    """Test retrieving all comments."""

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a GET request to retrieve all comments
        response = await ac.get("/comments/")

        assert response.status_code == 200

        cmt_response = response.json()
        assert isinstance(cmt_response, list)
        assert len(cmt_response) >= 0


@pytest.mark.anyio
async def test_get_all_comments_of_post(create_post, create_comment):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/comments/post/{create_post.id}")
        assert response.status_code == 200
        comments_response = response.json()
        assert isinstance(comments_response, list)
        assert len(comments_response) == 0


@pytest.mark.anyio
async def test_update_comment(create_comment):
    """Test to update a comment endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Send a PUT request to update a comment
        response = await ac.put(f"/comments/{create_comment.id}", json={
            "content": "Updated comment content"
        })
        assert response.status_code == 200
        comment_response = response.json()
        assert comment_response["content"] == "Updated comment content"


@pytest.mark.anyio
async def test_delete_comment(create_comment):
    """Test deleting a comment."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/comments/{create_comment.id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Comment deleted successfully"}

        # Verify the comment is deleted
        response = await ac.get(f"/comments/post/{create_comment.post_id}")
        assert response.status_code == 200
        comments_response = response.json()
        assert all(comment["id"] !=
                   create_comment.id for comment in comments_response)

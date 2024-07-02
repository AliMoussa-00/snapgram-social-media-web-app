#!/usr/bin/env python3
""" Defining Routes for the post class """

from beanie import DeleteRules
from fastapi import APIRouter, HTTPException, status, Depends
from app.api.dependencies import get_current_user
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post, PostCreateRequest, PostResponse, UpdatePostRequest
from app.models.user import User
from typing import List

post_router = APIRouter()


@post_router.post('/',
                  status_code=status.HTTP_201_CREATED,
                  response_description='Create Post')
async def create_post(
        post_create: PostCreateRequest,
        current_user: User = Depends(get_current_user)) -> PostResponse:
    """
    Create a new post
    """

    user = await User.get(post_create.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    post_data = post_create.model_dump(exclude_unset=True)
    post = Post(**post_data)
    await post.create()

    await user.add_post(post)

    return PostResponse(**post.model_dump(by_alias=True))


@post_router.get('/',
                 status_code=status.HTTP_200_OK,
                 response_description='Get All Post')
async def get_all_posts() -> List[PostResponse]:
    """Get all posts; !! will be removed"""
    posts = await Post.find().to_list()
    return [PostResponse(**post.model_dump(by_alias=True)) for post in posts]


@post_router.get('/user/{user_id}',
                 status_code=status.HTTP_200_OK,
                 response_description='Get all posts of a user')
async def get_all_posts_of_user(
        user_id: str,
        current_user: User = Depends(get_current_user)) -> List[PostResponse]:
    """Get all posts of a user"""
    user = await User.get(user_id, fetch_links=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    posts = user.posts
    # posts = await Post.find(Post.user_id == user_id).to_list()
    return [PostResponse(**post.model_dump(by_alias=True)) for post in posts]


@post_router.get('/{post_id}',
                 status_code=status.HTTP_200_OK,
                 response_description='Get Post By Id')
async def get_post_by_id(
        post_id: str,
        current_user: User = Depends(get_current_user)) -> PostResponse:
    """Get a post by id"""
    post = await Post.get(post_id, fetch_links=True)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found!"
        )
    return PostResponse(**post.model_dump(by_alias=True))


@post_router.put('/{post_id}',
                 status_code=status.HTTP_200_OK,
                 response_description='Update a post by ID')
async def update_post(
        post_id: str,
        updated_post: UpdatePostRequest,
        current_user: User = Depends(get_current_user)) -> PostResponse:
    """Update a post"""

    post = await Post.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    post_date = updated_post.model_dump(exclude_unset=True)
    post.update_timestamps()
    await post.set(post_date)
    return PostResponse(**post.model_dump(by_alias=True))


@post_router.delete('/{post_id}',
                    status_code=status.HTTP_200_OK,
                    response_description='Delete Post By Id')
async def delete_post_by_id(
        post_id: str,
        current_user: User = Depends(get_current_user)) -> dict:
    """Delete a post"""

    post = await Post.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found!"
        )
    await Like.find(Like.post_id == post.id).delete()
    await Comment.find(Comment.post_id == post.id).delete()
    await post.delete()
    await current_user.remove_post(post)
    # await post.delete(link_rule=DeleteRules.DELETE_LINKS)
    return {"message": "Post deleted successfully"}


# For Testing
@post_router.delete('/',
                    status_code=status.HTTP_200_OK,
                    response_description='Delete all post')
async def delete_all_post():
    """Delete all posts; !! will be removed"""
    try:
        # Fetch all posts
        posts = await Post.find().to_list()

        # Delete each post
        for post in posts:
            await post.delete()

        return {"message": "All posts deleted successfully"}
    except Exception as e:
        return {"error": f"Failed to delete posts: {e}"}

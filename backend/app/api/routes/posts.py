#!/usr/bin/env python3
""" Defining Routes for the post class """

from fastapi import APIRouter, HTTPException, status
from app.models.post import Post
from typing import List

post_router = APIRouter()


@post_router.post('/',
                  status_code=status.HTTP_201_CREATED,
                  response_description='Create Post')
async def create_post(post: Post) -> Post:
    try:
        await post.create()
        return post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@post_router.get('/',
                 status_code=status.HTTP_200_OK,
                 response_description='Get All Post')
async def get_all_posts() -> List[Post]:
    posts = await Post.find().to_list()
    return posts


@post_router.get('/user/{user_id}',
                 status_code=status.HTTP_200_OK,
                 response_description='Get All Post')
async def get_all_posts_of_user(user_id: str) -> List[Post]:
    pass


@post_router.get('/{id}',
                 status_code=status.HTTP_200_OK,
                 response_description='Get Post By Id')
async def get_post_by_id(id: str) -> Post:
    post = await Post.get(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found!"
        )
    return post


@post_router.delete('/{id}',
                    status_code=status.HTTP_200_OK,
                    response_description='Delete Post By Id')
async def delete_post_by_id(id: str) -> dict:
    post = await Post.get(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found!"
        )
    await post.delete()
    return {"message": "Post deleted successfully"}

#!/usr/bin/env python3
""" Defining Routes for the like class """

from fastapi import APIRouter, HTTPException, status, Depends
from app.api.dependencies import get_current_user
from app.models.like import Like, LikeCreateRequest, LikeResponse
from app.models.post import Post
from app.models.user import User
from typing import List

like_router = APIRouter()


@like_router.post('/',
                  status_code=status.HTTP_201_CREATED,
                  response_description='Like  Post')
async def like_post(like_create: LikeCreateRequest, current_user: User = Depends(get_current_user)) -> LikeResponse:
    post = await Post.get(like_create.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    user = await User.get(like_create.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    # Check if the user has already liked the post
    existing_like = await Like.find_one({"user_id": like_create.user_id, "post_id": like_create.post_id})
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User has already liked this post'
        )

    like_data = like_create.model_dump(exclude_unset=True)
    like = Like(**like_data)
    await like.create()

    await post.add_like(like)

    return LikeResponse(**like.model_dump(by_alias=True))


@like_router.delete('/{like_id}',
                    status_code=status.HTTP_200_OK,
                    response_description='Unlike Post')
async def unlike_post(like_id: str, current_user: User = Depends(get_current_user)) -> dict:
    like = await Like.get(like_id)
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Like not found'
        )

    post = await Post.get(like.post_id, fetch_links=True)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )

    await like.delete()
    await post.remove_like(like)

    return {"message": "Like deleted successfully"}


@like_router.get('/post/{post_id}',
                 status_code=status.HTTP_200_OK,
                 response_description='Get all likes of a post')
async def get_all_likes_of_post(post_id: str, current_user: User = Depends(get_current_user)) -> List[LikeResponse]:
    post = await Post.get(post_id, fetch_links=True)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )

    likes = post.likes

    return [LikeResponse(**like.model_dump(by_alias=True)) for like in likes]

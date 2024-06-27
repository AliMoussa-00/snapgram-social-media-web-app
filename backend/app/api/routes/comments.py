#!/usr/bin/env python3
""" Defining Routes for the comment class """

from fastapi import APIRouter, status, HTTPException
from app.models.comment import Comment, CommentCreateRequest, UpdateCommentRequest, CommentResponse
from app.models.post import Post
from app.models.user import User
from typing import List


comment_router = APIRouter()


@comment_router.post('/',
                     status_code=status.HTTP_201_CREATED,
                     response_description='Create Comment')
async def create_comment(comment_create: CommentCreateRequest) -> CommentResponse:
    post = await Post.get(comment_create.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    user = await User.get(comment_create.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    comment_data = comment_create.model_dump(exclude_unset=True)
    comment = Comment(**comment_data)
    await comment.create()

    await post.add_comment(comment)

    return CommentResponse(**comment.model_dump(by_alias=True))


@comment_router.get('/',
                    status_code=status.HTTP_200_OK,
                    response_description='Get All Comment')
async def get_all_comments() -> List[CommentResponse]:
    comments = await Comment.find().to_list()
    return [CommentResponse(**comment.model_dump(by_alias=True)) for comment in comments]


@comment_router.get('/post/{post_id}',
                    status_code=status.HTTP_200_OK,
                    response_description='Get all comments of a post')
async def get_all_comments_of_post(post_id: str) -> List[CommentResponse]:
    post = await Post.get(post_id, fetch_links=True)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )

    comments = post.comments

    return [CommentResponse(**comment.model_dump(by_alias=True)) for comment in comments]


@comment_router.put('/{comment_id}',
                    status_code=status.HTTP_200_OK,
                    response_description='Update a comment by ID')
async def update_comment(comment_id: str, update_comment: UpdateCommentRequest) -> CommentResponse:
    comment = await Comment.get(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    comment_data = update_comment.model_dump(exclude_unset=True)
    comment.update_timestamps()
    await comment.set(comment_data)
    return CommentResponse(**comment.model_dump(by_alias=True))


@comment_router.delete('/{comment_id}',
                       status_code=status.HTTP_200_OK,
                       response_description='Delete a comment by ID')
async def delete_comment(comment_id: str) -> dict:
    comment = await Comment.get(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    post = await Post.get(comment.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    await comment.delete()
    await post.remove_comment(comment)
    return {"message": "Comment deleted successfully"}


# For Testing
@comment_router.delete('/',
                       status_code=status.HTTP_200_OK,
                       response_description='Delete all comment')
async def delete_all_comments():
    try:
        # Fetch all comments
        comments = await Comment.find().to_list()

        # Delete each comment
        for comment in comments:
            await comment.delete()

        return {"message": "All comments deleted successfully"}
    except Exception as e:
        return {"error": f"Failed to delete comments: {e}"}

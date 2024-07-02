#!/usr/bin/env python3
""" Defining Routes for the user class """

from typing import List
from beanie import DeleteRules
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.comment import Comment
from app.models.like import Like
from app.models.user import User, UserResponse, UpdateUserRequest
from app.api.dependencies import get_current_user
from app.utils.auth import hash_password

user_router = APIRouter()


@user_router.get('/',
                 response_model=List[UserResponse])
async def get_all_users(current_user: User = Depends(get_current_user)) -> List[UserResponse]:
    """Get all users"""
    users = await User.find().to_list()
    return [UserResponse(**user.model_dump(by_alias=True)) for user in users]


@user_router.get('/{user_id}',
                 response_model=UserResponse)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get a user by ID"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return UserResponse(**user.model_dump(by_alias=True))


@user_router.put('/{user_id}',
                 response_model=UserResponse)
async def update_user(user_id: str, updated_user: UpdateUserRequest, current_user: User = Depends(get_current_user)) -> UserResponse:
    """Update a user by ID"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user_data = updated_user.model_dump(exclude_unset=True)
    if 'password' in user_data:
        user_data['hashed_password'] = hash_password(user_data.pop('password'))

    user.update_timestamps()
    await user.set(user_data)

    return UserResponse(**user.model_dump(by_alias=True))


@user_router.post('/follow/{friend_id}',
                  status_code=status.HTTP_200_OK,
                  response_description='follow user')
async def follow_user(friend_id: str, current_user: User = Depends(get_current_user)) -> dict:
    friend = await User.get(friend_id, fetch_links=True)
    if not friend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Friend not found')

    current_user.following.append(friend)
    friend.followers.append(current_user)

    await current_user.save()
    await friend.save()

    return {"message": "follow successfully"}


@user_router.get('/{user_id}/followers',
                 status_code=status.HTTP_200_OK,
                 response_description='List followers')
async def get_followers(user_id: str, current_user: User = Depends(get_current_user)) -> List[UserResponse]:
    user = await User.get(user_id, fetch_links=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user.followers


@user_router.get('/{user_id}/following',
                 status_code=status.HTTP_200_OK,
                 response_description='List following')
async def get_following(user_id: str, current_user: User = Depends(get_current_user)) -> List[UserResponse]:
    user = await User.get(user_id, fetch_links=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user.following


@user_router.delete('/unfollow/{friend_id}',
                    status_code=status.HTTP_200_OK,
                    response_description='Unfollow user')
async def unfollow_user(friend_id: str, current_user: User = Depends(get_current_user)) -> dict:
    friend = await User.get(friend_id, fetch_links=True)
    if not friend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Friend not found')
    current_user.following = [
        u for u in current_user.following if u.id != friend_id]
    friend.followers = [u for u in friend.followers if u.id != current_user.id]

    await current_user.save()
    await friend.save()

    return {"message": "Unfollowed successfully"}


@user_router.delete('/{user_id}',
                    status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)) -> dict:
    """Delete a user by ID"""
    user = await User.get(user_id, fetch_links=True, nesting_depth=1)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    # Get all posts of this user
    posts = user.posts
    for post in posts:
        await Comment.find(Comment.post_id == post.id).delete()
        await Like.find(Like.post_id == post.id).delete()
        await post.delete()
        await user.remove_post(post)
    # Delete the user
    await user.delete()
    return {"message": "user deleted successfully"}


# For Testing
@user_router.delete('/',
                    status_code=status.HTTP_200_OK,
                    response_description='Delete all user')
async def delete_all_users():
    try:
        # Fetch all users
        users = await User.find().to_list()

        # Delete each users
        for user in users:
            await user.delete()

        return {"message": "All users deleted successfully"}
    except Exception as e:
        return {"error": f"Failed to delete users: {e}"}

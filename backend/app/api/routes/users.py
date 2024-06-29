#!/usr/bin/env python3
""" Defining Routes for the user class """

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import User, UserResponse, UpdateUserRequest
from app.api.dependencies import get_current_user
from app.utils.auth import hash_password

router = APIRouter()


@router.get('/',
            response_model=List[UserResponse])
async def get_all_users(current_user: User = Depends(get_current_user)) -> List[UserResponse]:
    """Get all users"""
    users = await User.find().to_list()
    return [UserResponse(**user.model_dump(by_alias=True)) for user in users]


@router.get('/{user_id}',
            response_model=UserResponse)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get a user by ID"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return UserResponse(**user.model_dump(by_alias=True))


@router.put('/{user_id}',
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


@router.delete('/{user_id}',
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)) -> None:
    """Delete a user by ID"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    await user.delete()


# For Testing
@router.delete('/',
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

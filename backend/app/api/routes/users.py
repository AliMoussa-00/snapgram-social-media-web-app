#!/usr/bin/env python3
""" Defining Routes for the user class """

from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.user import User, UserCreateRequest, UserResponse, UpdateUserRequest
from app.utils.hashing import hash_password

router = APIRouter()


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_description='create a user',
             response_model=UserResponse)
async def create_user(user_create: UserCreateRequest) -> UserResponse:
    user_data = user_create.model_dump(exclude_unset=True)
    if 'password' in user_data:
        user_data['hashed_password'] = hash_password(user_data.pop('password'))

    user = User(**user_data)
    await user.create()
    return UserResponse(**user.model_dump(by_alias=True))


@router.get('/',
            status_code=status.HTTP_200_OK,
            response_description='get all users as a list',
            response_model=List[UserResponse])
async def get_all_users() -> List[UserResponse]:
    users = await User.find().to_list()
    return [UserResponse(**user.model_dump(by_alias=True)) for user in users]


@router.get('/{user_id}',
            response_description='get a user based on id',
            response_model=UserResponse)
async def get_user(user_id: str) -> UserResponse:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return UserResponse(**user.model_dump(by_alias=True))


@router.put('/{user_id}',
            response_description='updating a user',
            response_model=UserResponse)
async def update_user(user_id: str, updated_user: UpdateUserRequest) -> UserResponse:
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
               status_code=status.HTTP_204_NO_CONTENT,
               response_description='deleting a user')
async def delete_user(user_id: str) -> None:
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

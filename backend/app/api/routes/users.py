#!/usr/bin/env python3
""" Defining Routes for the user class """

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.models.user import User

router = APIRouter()


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_description='create a user',
             response_model=User)
async def create_user(user: User) -> User:
    await user.create()
    return user


@router.get('/',
            status_code=status.HTTP_200_OK,
            response_description='get all users as a list',
            response_model=List[User])
async def get_all_users() -> List[User]:
    users = await User.find().to_list()
    return users


@router.get('/{user_id}',
            response_description='get a user based on id',
            response_model=User)
async def get_user(user_id: str) -> User:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user


# Update the user
class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None


@router.put('/{user_id}',
            response_description='updating a user',
            response_model=User)
async def update_user(user_id: str, updated_user: UpdateUserRequest) -> User:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user_data = updated_user.model_dump(exclude_unset=True)
    if 'password' in user_data:
        # !! I should hash the password
        user_data['hashed_password'] = user_data.pop('password')

    user.update_timestamps()
    await user.set(user_data)

    return user


@router.delete('/{user_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               response_description='deleting a user')
async def delete_user(user_id: str) -> None:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    await user.delete()

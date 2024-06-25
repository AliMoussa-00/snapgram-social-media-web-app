#!/usr/bin/env python3
"""Authentication routes for user sign-up and login"""

from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User, UserCreateRequest, UserResponse
from app.utils.auth import hash_password, verify_password, create_access_token, create_refresh_access_token
from fastapi import APIRouter, HTTPException, status, Depends
from app.api.dependencies import get_current_user, oauth2_scheme
from pydantic import BaseModel
from app.models.token import Token, BlackListedTokens


router = APIRouter()


@router.post('/register',
             status_code=status.HTTP_201_CREATED,
             response_description='Register a new user',
             response_model=Token)
async def sign_up(user_create: UserCreateRequest) -> Token:
    """Register a new user"""
    user_data = user_create.model_dump(exclude_unset=True)

    exist_user_with_email = await User.find_one(User.email == user_data['email'])
    if exist_user_with_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    exist_user_with_username = await User.find_one(User.username == user_data['username'])
    if exist_user_with_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='username already registered')

    if 'password' in user_data:
        user_data['hashed_password'] = hash_password(user_data.pop('password'))

    user = User(**user_data)
    await user.create()

    payload = {
        "user_id": user.id,
        "email": user.email
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_access_token(payload)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type=None)


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login the user

    # form_data will automatically have 'username/email' and 'password' attributes
    """

    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    payload = {
        "user_id": user.id,
        "email": user.email
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_access_token(payload)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type=None)


@router.get('/me',
            response_description="get the current authenticated user",
            response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)) -> UserResponse:
    """get the current authenticated user"""

    return UserResponse(**current_user.model_dump(by_alias=True))


@router.post('/logout',
             response_description="logout a user",
             response_model=dict)
async def logout_user(
        current_user: User = Depends(get_current_user),
        token: str = Depends(oauth2_scheme)) -> dict:
    """logout a user"""
    black_listed_token = BlackListedTokens(token=token)
    await black_listed_token.create()
    return {"message": "Successfully logged out"}

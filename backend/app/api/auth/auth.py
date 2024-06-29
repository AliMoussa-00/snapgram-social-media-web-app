#!/usr/bin/env python3
"""Authentication routes for user sign-up and login"""

from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from app.core.config import CONFIG
from app.models.user import User, UserCreateRequest, UserResponse
from app.utils.auth import hash_password, verify_password, create_access_token, create_refresh_access_token
from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.api.dependencies import get_current_user, oauth2_scheme
from pydantic import EmailStr
from app.models.token import Token, BlackListedTokens
from app.utils.mail import send_password_reset_email


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
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
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


# Body(..., embed=True) means that this parameter must be included in the request body
# and should be embedded under a single key.
@router.post('/forgot-password',
             status_code=status.HTTP_200_OK,
             response_model=dict)
async def forgot_password(email: EmailStr = Body(..., embed=True)) -> dict:
    """Send password reset email."""
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(404, "No user found with that email")

    payload = {"email": user.email}
    token = create_access_token(payload)

    await send_password_reset_email(email, token)

    # print the token so i can use it in the next request
    # print(f"XXXXX: reset token = {token}\n")
    return {"message": "Message sent to user's email successfully"}


@router.post("/reset-password/{token}",
             status_code=status.HTTP_200_OK,
             response_model=Token)
async def reset_password(token: str, new_pwd: str = Body(..., embed=True)) -> Token:
    """reset the user's password"""

    user = await get_current_user(token)
    if not user:
        raise HTTPException(404, "No user found with that email")

    user.hashed_password = hash_password(new_pwd)
    await user.save()

    # creating new tokens and login the user
    payload = {
        "user_id": user.id,
        "email": user.email
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_access_token(payload)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type=None)


@router.post('/refresh-token', response_model=Token)
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    """
    Refresh the access token using the refresh token.

    Args:
        refresh_token (str): The refresh token.

    Returns:
        Token: New access token and refresh token.
    """
    try:
        payload = decode(
            refresh_token, CONFIG.jwt_refresh_secret_key, algorithms=["HS256"])

        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if user_id:
            user = await User.get(user_id)
        else:
            user = await User.find_one(User.email == email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Issue new tokens
        new_payload = {"user_id": user.id, "email": user.email}
        new_access_token = create_access_token(new_payload)
        new_refresh_token = create_refresh_access_token(new_payload)
        return Token(access_token=new_access_token, refresh_token=new_refresh_token, token_type="Bearer")

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

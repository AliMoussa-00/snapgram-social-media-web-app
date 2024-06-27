#!/usr/bin/env python3
"""Defining hashing and token generation functions"""

from datetime import datetime, timedelta
from typing import Optional
import bcrypt
import jwt
from app.core.config import CONFIG


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Hashes the provided password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def verify_password(password: str, hashed_password) -> bool:
    """
    Verifies a password against a hashed password using bcrypt.

    Args:
        password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_access_token(payload: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.

    Args:
        payload (dict): The data to encode in the token.
        expires_delta (Optional[timedelta]): The time delta for token expiration.

    Returns:
        str: The encoded JWT token.
    """

    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, key=CONFIG.jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_access_token(payload: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT refresh token.

    Args:
        payload (dict): The payload to encode in the token.
        expires_delta (Optional[timedelta]): The time delta for token expiration.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, key=CONFIG.jwt_refresh_secret_key, algorithm=ALGORITHM)
    return encoded_jwt

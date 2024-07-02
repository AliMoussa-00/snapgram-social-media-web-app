#!/usr/bin/env python3
"""Dependencies for secured routes"""

from app.models.user import User
from app.models.token import BlackListedTokens
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import CONFIG
import jwt

# typically used for routes that require OAuth2-style authentication using username/email and password.
# It expects the token to be provided in the Authorization header of the HTTP request.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login', scheme_name="JWT")

ALGORITHM = "HS256"


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to retrieve the current authenticated user based on the JWT token.

    Args:
        token (str): JWT token extracted from the Authorization header.

    Returns:
        User: Authenticated user object if the token is valid and corresponds to an existing user.

    Raises:
        HTTPException: If the token is invalid or doesn't correspond to a valid user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # check if token is black listed
    is_blacklisted = await BlackListedTokens.is_token_blacklisted(token)
    if is_blacklisted:
        raise credentials_exception

    try:
        payload = jwt.decode(token, CONFIG.jwt_secret_key, ALGORITHM)
        email: str = payload.get('email', None)
        user_id: str = payload.get('user_id', None)
        if not email and not user_id:
            raise credentials_exception
    except (jwt.PyJWTError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise credentials_exception

    if user_id:
        # get user by id
        user = await User.get(user_id, fetch_links=True, nesting_depth=1)
    else:
        # get user by email
        user = await User.find_one(User.email == email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )
    return user

#!/usr/bin/env python3
""" Defining the User module """

from beanie import Link
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from app.models.common import Common
from datetime import datetime

from app.models.post import Post


class User(Common):
    """
    Represents a user in the application.

    Attributes:
        email (EmailStr): Email address of the user.
        hashed_password (str): Hashed password for user authentication.
        username (str): Unique username for the user.
        full_name (Optional[str], optional): Full name of the user.
        bio (Optional[str], optional): Biography or profile description of the user.
        profile_picture_url (Optional[str], optional): URL or path to the user's profile picture.

        posts: a list of posts created by the user, it is linked to the Post class, 
        followers: a list of users following the current user, it is linked to the User class, 
        following: a list of users the current user is following, it is linked to the User class, 

    Settings:
        name (str): MongoDB collection name for storing User documents.
    """

    email: EmailStr
    hashed_password: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    posts: Optional[List[Link["Post"]]] = []
    followers: Optional[List[Link["User"]]] = []
    following: Optional[List[Link["User"]]] = []

    class Settings:
        """
        Settings for the User class.

        Attributes:
            name (str): Name of the MongoDB collection where User documents are stored.
        """
        name = 'users'

    async def add_post(self, post: Post):
        """
        Add a post to user.posts
        when a user creates a post, it will be created, stored
        and appended to the list of posts of the user
        """

        self.posts.append(post)
        await self.save()

    async def remove_post(self, post: Post):
        """
        Remove a post from the list of user.posts
        when a post is removed from db it should also be removed from user.posts
        """

        self.posts = [pt for pt in self.posts if pt.id != post.id]
        await self.save()


class UserCreateRequest(BaseModel):
    """
    User creation request model for POST requests.

    Attributes:
    - email: The user's email address.
    - password: The user's password (to be hashed before storing).
    - username: The user's username.
    - full_name: The user's full name (optional).
    - bio: A short biography of the user (optional).
    - profile_picture_url: URL to the user's profile picture (optional).
    """
    email: EmailStr
    password: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UpdateUserRequest(BaseModel):
    """
    User update request model for PUT requests.

    Attributes:
    - email: The user's email address (optional).
    - password: The user's password (optional, to be hashed before storing).
    - username: The user's username (optional).
    - full_name: The user's full name (optional).
    - bio: A short biography of the user (optional).
    - profile_picture_url: URL to the user's profile picture (optional).
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserResponse(BaseModel):
    """
    User response model for API responses.

    Attributes:
    - id: The user's ID.
    - email: The user's email address.
    - username: The user's username.
    - full_name: The user's full name (optional).
    - created_at: The timestamp when the user was created (optional).
    - updated_at: The timestamp when the user was last updated (optional).
    - bio: A short biography of the user (optional).
    - profile_picture_url: URL to the user's profile picture (optional).
    """
    id: Optional[str] = Field(alias="_id")
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        str_strip_whitespace = True
        json_encoders = {
            datetime: lambda date: date.isoformat(),
        }

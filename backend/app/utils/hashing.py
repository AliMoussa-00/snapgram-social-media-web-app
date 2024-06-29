#!/usr/bin/env python3


import bcrypt


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
    Verifies the provided password against the hashed password.

    Args:
        password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

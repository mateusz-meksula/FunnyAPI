import string

from fastapi import HTTPException, status
from jose import jwt
from passlib.hash import pbkdf2_sha256


class AuthenticationError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class CredentialsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_password(password: str) -> str:
    has_min_len = len(password) >= 10
    if not has_min_len:
        raise ValueError("Password must be at least 10 characters long.")

    has_uppercase_and_lowercase = (password.lower() != password) and (
        password.upper() != password
    )
    if not has_uppercase_and_lowercase:
        raise ValueError(
            "Password must contain both lowercase and uppercase characters."
        )

    unique_chars = set(password)

    has_different_chars = len(unique_chars) >= len(password) / 2
    if not has_different_chars:
        raise ValueError(
            "Password must contain a sufficient number of unique characters."
        )

    has_special_chars = bool(set(string.punctuation) & unique_chars)
    if not has_special_chars:
        raise ValueError("Password must contain at least one special character.")

    has_numbers = bool(set("1234567890") & unique_chars)
    if not has_numbers:
        raise ValueError("Password must contain at least one number.")

    return password


def get_password_hash(password: str):
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(password, hash)


def create_jwt_token(payload: dict, key: str, algorithm: str) -> str:
    return jwt.encode(
        claims=payload.copy(),
        key=key,
        algorithm=algorithm,
    )

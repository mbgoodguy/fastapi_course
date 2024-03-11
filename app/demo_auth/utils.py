import datetime
from datetime import timedelta, datetime

import bcrypt

import jwt
from core.config import settings

SECRET_KEY = 'mysecretkey'
ALGORITHM = 'HS256'
USERS_DATA = [
    {'username': 'admin', 'password': 'adminpass'},
]


def encode_jwt(
        payload: dict,
        key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, key, algorithm=algorithm)

    return encoded


def decode_jwt(
        token: str,
        key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(token, key, algorithms=[algorithm])

    return decoded


def hash_pwd(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_pwd(pwd: str, hashed_pwd: bytes) -> bool:
    return bcrypt.checkpw(pwd.encode(), hashed_password=hashed_pwd)

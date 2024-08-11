import jwt
import random
import string
from hashlib import md5
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class CredentialsExeption(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


def generate_random_salt() -> str:
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=settings.auth.salt_len)
    )


async def generate_password_hash(password: str, salt: str) -> str:
    dynamic_salt = salt.encode()
    server_salt = settings.auth.salt.encode()
    password_hash = md5(password.encode())

    for _ in range(settings.auth.repeat):
        password_hash.update(dynamic_salt)
        password_hash.update(server_salt)
        password_hash = md5(password_hash.digest())

    return password_hash.hexdigest()


async def validate_password(password, password_hash, salt) -> bool:
    return password_hash == await generate_password_hash(password, salt)


def create_jwt_token(data: dict, life_time: timedelta | None = None) -> str:
    encode = data.copy()
    expire = datetime.now(timezone.utc)
    if not life_time:
        life_time = timedelta(minutes=settings.auth.token_life_time)
    expire += life_time
    encode.update({"exp": expire})
    return jwt.encode(encode, settings.auth.secret, algorithm=settings.auth.algorithm)


def get_user_from_token(token: str = Depends(oauth2_scheme)) -> str:
    exception = CredentialsExeption("Could not validate credentials")
    try:
        payload = jwt.decode(
            token, settings.auth.secret, algorithms=[settings.auth.algorithm]
        )
        username = payload.get("sub")
        if not username:
            raise exception
        return username
    except jwt.ExpiredSignatureError:
        raise exception
    except jwt.InvalidTokenError:
        raise exception

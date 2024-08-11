import jwt
import random
import string
from hashlib import md5
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class CredentialsExeption(HTTPException):
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def generate_random_salt() -> str:
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=settings.auth.salt_len)
    )


def generate_password_hash(password: str, salt: str):
    dynamic_salt = salt.encode()
    server_salt = settings.auth.salt.encode()
    password_hash = md5(password.encode())

    for _ in range(settings.auth.repeat):
        password_hash.update(dynamic_salt)
        password_hash.update(server_salt)
        password_hash = md5(password_hash.digest())

    return password_hash.hexdigest()


def validate_password(password, password_hash, salt):
    return generate_password_hash(password, salt) == password_hash


def create_jwt_token(data: dict):
    return jwt.encode(data, settings.auth.secret, algorithms=[settings.auth.algorithm])


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    exception = CredentialsExeption(
        "Could not validate credentials", headers={"WWW-authenticate": "Bearer"}
    )
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

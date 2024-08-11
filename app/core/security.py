from app.core.config import settings
import random
import string
from hashlib import md5


def generate_random_salt() -> str:
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=settings.auth.salt_len)
    )


async def generate_password_hash(password: str, salt: str):
    dynamic_salt = salt.encode()
    server_salt = settings.auth.salt.encode()
    password_hash = md5(password.encode())

    for _ in range(settings.auth.repeat):
        password_hash.update(dynamic_salt)
        password_hash.update(server_salt)
        password_hash = md5(password_hash)

    return password_hash.hexdigest()
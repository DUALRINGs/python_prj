from datetime import datetime, timedelta
from typing import Optional
from authlib.jose import JsonWebToken as authlib_jwt
from passlib.context import CryptContext
from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def encode_jwt(
    payload: dict,
    private_key: str = None,
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
) -> str:
    if private_key is None:
        with open(settings.auth_jwt.private_key_path, "r") as f:
            private_key = f.read()

    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )

    jwt_instance = authlib_jwt([algorithm])

    encoded = jwt_instance.encode(
        {"alg": algorithm},  # Заголовок
        to_encode,           # Полезная нагрузка
        private_key,         # Приватный ключ
    )
    return encoded.decode("utf-8")

async def decode_jwt(
    token: str | bytes,
    public_key: str = None,
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    if public_key is None:
        with open(settings.auth_jwt.public_key_path, "r") as f:
            public_key = f.read()

    # Создаем объект JsonWebToken
    jwt_instance = authlib_jwt([algorithm])

    # Декодируем токен
    decoded = jwt_instance.decode(token, public_key)
    decoded.validate()  # Проверяем валидность токена

    return decoded


async def hash_password(
    password: str,
) -> str:
    hashed = await pwd_context.hash(password)
    return hashed


async def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    is_valid = await pwd_context.verify(password, hashed_password)
    return is_valid
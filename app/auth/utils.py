from datetime import datetime, timedelta
from typing import Optional, Union
import jwt  # Используем PyJWT для работы с JWT
from passlib.context import CryptContext
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def encode_jwt(
    payload: dict,
    private_key: str = None,
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
) -> str:
    """
    Генерирует JWT-токен на основе переданных данных.

    :param payload: Данные для включения в токен.
    :param private_key: Приватный ключ для подписи токена. Если не указан, читается из файла.
    :param algorithm: Алгоритм подписи токена.
    :param expire_minutes: Время жизни токена в минутах.
    :param expire_timedelta: Время жизни токена в виде timedelta.
    :return: Сгенерированный JWT-токен.
    """
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

    token = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return token


async def decode_jwt(
    token: Union[str, bytes],
    public_key: str = None,
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """
    Декодирует JWT-токен и возвращает его payload.

    :param token: JWT-токен для декодирования.
    :param public_key: Публичный ключ для проверки подписи. Если не указан, читается из файла.
    :param algorithm: Алгоритм подписи токена.
    :return: Payload токена.
    :raises ValueError: Если токен недействителен или истек срок его действия.
    """
    if public_key is None:
        with open(settings.auth_jwt.public_key_path, "r") as f:
            public_key = f.read()

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")


def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.

    :param password: Пароль для хэширования.
    :return: Хэшированный пароль.
    """
    return pwd_context.hash(password)


def validate_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли пароль хэшированному значению.

    :param password: Пароль для проверки.
    :param hashed_password: Хэшированный пароль.
    :return: True, если пароль верный, иначе False.
    """
    return pwd_context.verify(password, hashed_password)
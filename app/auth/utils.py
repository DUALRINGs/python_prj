from datetime import datetime, timedelta
from typing import Optional
import jwt  # Используем PyJWT вместо authlib.jose
from passlib.context import CryptContext
from config import settings

# Настройка CryptContext для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def encode_jwt(
    payload: dict,
    private_key: str = None,
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
) -> str:
    """
    Генерирует JWT токен с использованием PyJWT.
    """
    if private_key is None:
        with open(settings.auth_jwt.private_key_path, "r") as f:
            private_key = f.read()

    # Добавляем время истечения токена
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

    # Генерируем токен
    token = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return token

async def decode_jwt(
    token: str | bytes,
    public_key: str = None,
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """
    Декодирует и проверяет JWT токен с использованием PyJWT.
    """
    if public_key is None:
        with open(settings.auth_jwt.public_key_path, "r") as f:
            public_key = f.read()

    try:
        # Декодируем токен
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

def hash_password(
    password: str,
) -> str:
    """
    Хеширует пароль с использованием bcrypt.
    """
    return pwd_context.hash(password)

def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    """
    Проверяет, соответствует ли пароль хешированному паролю.
    """
    return pwd_context.verify(password, hashed_password)
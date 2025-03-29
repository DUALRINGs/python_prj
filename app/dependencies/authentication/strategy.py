from fastapi_users.authentication import JWTStrategy
from app.config import settings


def get_jwt_strategy() -> JWTStrategy:
    """Создает и возвращает стратегию JWT-аутентификации.

    Читает приватный и публичный ключи из файлов, указанных в настройках,
    и инициализирует JWTStrategy с параметрами:
    - Алгоритмом подписи из настроек
    - Временем жизни токена
    - Ключами подписи/верификации

    Returns:
        Готовая стратегия для работы с JWT-токенами.

    Note:
        Требует наличия файлов с ключами по путям из настроек.
    """
    with open(settings.access_token.private_key_path, "r") as f:
        private_key = f.read()

    with open(settings.access_token.public_key_path, "r") as f:
        public_key = f.read()

    return JWTStrategy(
        secret=private_key,
        algorithm=settings.access_token.algorithm,
        lifetime_seconds=settings.access_token.access_token_expire_seconds,
        public_key=public_key,
    )

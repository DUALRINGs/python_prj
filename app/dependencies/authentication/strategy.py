from fastapi_users.authentication import JWTStrategy
from app.config import settings


def get_jwt_strategy() -> JWTStrategy:
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

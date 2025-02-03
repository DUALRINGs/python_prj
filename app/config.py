from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    """
    Настройки для JWT (JSON Web Token).

    :param private_key_path: Путь к файлу с приватным ключом.
    :param public_key_path: Путь к файлу с публичным ключом.
    :param algorithm: Алгоритм подписи токена.
    :param access_token_expire_minutes: Время жизни токена в минутах.
    """
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15

@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings, AuthJWT):
    db_url: str
    db_echo: bool
    auth_jwt: AuthJWT = AuthJWT()

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()

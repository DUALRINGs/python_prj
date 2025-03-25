from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


BASE_DIR = Path(__file__).parent.parent

class AccessTokenConfig(BaseModel):
    """
    Настройки для JWT (JSON Web Token).

    :param private_key_path: Путь к файлу с приватным ключом.
    :param public_key_path: Путь к файлу с публичным ключом.
    :param algorithm: Алгоритм подписи токена.
    :param access_token_expire_seconds: Время жизни токена в секундах.
    """
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_seconds: int = 960

@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    filename = f".env.{runtime_env}" if runtime_env else ".env"
    env_path = BASE_DIR / filename
    return str(env_path)

class EnvironmentSettings(BaseSettings, AccessTokenConfig):
    db_url: str
    db_echo: bool
    access_token: AccessTokenConfig = AccessTokenConfig()

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"

@lru_cache
def get_environment_variables():
    return EnvironmentSettings()

settings = get_environment_variables()

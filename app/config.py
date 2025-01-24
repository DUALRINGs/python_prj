from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


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


class Settings(BaseSettings):
    """
    Основные настройки приложения.

    :param db_url: URL для подключения к базе данных (читается из переменной окружения DB_URL).
    :param db_echo: Флаг для вывода SQL-запросов в консоль.
    :param auth_jwt: Настройки JWT.
    """
    db_url: str = Field(default="postgresql+asyncpg://root:xmen1904@localhost:5432/test_db", env="DB_URL")
    db_echo: bool = True
    auth_jwt: AuthJWT = AuthJWT()

    class Config:
        env_prefix = "APP_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
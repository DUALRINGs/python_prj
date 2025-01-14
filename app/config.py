from pydantic_settings import BaseSettings


class Setting(BaseSettings):
	db_url: str = 'postgresql+asyncpg://root:xmen1904@localhost:5432/test_db'
	db_echo: bool = True

settings = Setting()
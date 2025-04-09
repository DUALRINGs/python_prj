from typing import AsyncGenerator
from app.config import settings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


class DatabaseHelper:
    """Менеджер для работы с асинхронной БД через SQLAlchemy.

    Обеспечивает:
    - Создание и управление асинхронным engine
    - Фабрику сессий с оптимальными настройками
    - Генератор сессий для DI (dependency injection)
    - Корректное освобождение ресурсов

    Args:
        url: URL подключения к БД
        echo: Логирование SQL-запросов
        echo_pool: Логирование работы пула соединений
        pool_size: Размер пула соединений
        max_overflow: Максимальное overflow соединений

    Usage:
        db_helper = DatabaseHelper(url="postgresql+asyncpg://...")
        session = await db_helper.session_getter()
    """
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """Закрывает все соединения с БД."""
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """Генератор сессий для FastAPI Depends."""
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

db_helper = DatabaseHelper(
    url=str(settings.db_url),
    echo=settings.db_echo,
)

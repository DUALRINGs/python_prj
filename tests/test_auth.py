import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Использование одного event loop для всех тестов."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    """
    Фикстура для создания асинхронного HTTP-клиента.
    """
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture
async def user_data() -> dict:
    """
    Фикстура с данными для создания пользователя.
    """
    return {
        "name": "testuser",
        "email": "testtest@example.com",
        "password": "test_password",
    }


@pytest_asyncio.fixture
async def auth(client: AsyncClient, user_data: dict) -> dict:
    """
    Фикстура для аутентификации пользователя и получения токена.
    """
    # Создание пользователя
    await client.post("/auth/register", json=user_data)

    # Аутентификация и получение токена
    response = await client.post("/auth/login", data={"username": user_data["email"], "password": user_data["password"]})

    assert response.status_code == 200, f"Authentication failed: {response.text}"
    return response.json()  # Токен будет в ответе, например, response.json()["access_token"]
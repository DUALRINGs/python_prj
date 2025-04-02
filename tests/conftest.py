import asyncio
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
        "password": "user_password",
        "name": "test_user",
        "id": 1,
        "email": "user@example.com",
        "is_active": 'true',
        "is_superuser": 'false',
        "is_verified": 'false',
    }

@pytest_asyncio.fixture
async def admin_data() -> dict:
    """
    Фикстура с данными админа.
    """
    return {
        "name": "admin",
        "email": "admin@mail.com",
        "password": "admin",
    }

@pytest_asyncio.fixture
async def task_data() -> dict:
    """
    Фикстура с данными для создания задачи.
    """
    return {
        "title": "test_tusk",
        "description": "test_task_1",
        "status": "новая",
    }

@pytest_asyncio.fixture
async def token(client: AsyncClient, user_data: dict) -> dict:
    """
    Фикстура для аутентификации пользователя и получения токена.
    """
    # Создание пользователя
    await client.post("/auth/register", json=user_data)

    # Аутентификация и получение токена
    response = await client.post("/auth/login", data={"username": user_data["email"], "password": user_data["password"]})

    assert response.status_code == 200, f"Authentication failed: {response.text}"
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def admin_token(client: AsyncClient, admin_data: dict) -> dict:
    """
    Фикстура для аутентификации пользователя и получения токена админа.
    """
    response = await client.post("/auth/login", data={"username": admin_data["email"], "password": admin_data["password"]})

    assert response.status_code == 200, f"Authentication failed: {response.text}"
    return response.json()["access_token"]

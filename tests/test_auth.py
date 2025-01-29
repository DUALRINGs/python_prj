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

@pytest.mark.asyncio
async def test(client: AsyncClient):
    """
    Тест для проверки GET-запроса на корневой URL.
    """
    response = await client.get("/users/")
    assert response.status_code == 200

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

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """
    Тест для создания пользователя через POST-запрос.
    """
    json = {
        "name": "strgs",
        "email": "ussrsgser@example.com",
        "password": "stegeing"
    }

    response = await client.post("/users/", json=json)
    assert response.status_code == 200 or 409


@pytest.mark.asyncio
async def test_create_existing_user(client: AsyncClient):
    """
    Тест для создания пользователя через POST-запрос.
    """
    json = {
        "name": "strgs",
        "email": "ussrsgser@example.com",
        "password": "stegeing"
    }

    response = await client.post("/users/", json=json)
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_read_users(client: AsyncClient):
    response = await client.get("/users/")
    assert response.status_code == 200

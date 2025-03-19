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


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, user_data: dict):
    """
    Тест регистрации нового пользователя.
    """
    response = await client.post("/auth/register", json=user_data)

    # Проверяем, что статус код 200 (или 201, если используется для создания)
    assert response.status_code == 200, f"Registration failed: {response.text}"

    # Проверяем, что в ответе есть данные пользователя
    response_data = response.json()
    assert "email" in response_data
    assert response_data["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, user_data: dict):
    """
    Тест аутентификации пользователя.
    """
    # Сначала регистрируем пользователя
    await client.post("/auth/register", json=user_data)

    # Пытаемся аутентифицироваться
    response = await client.post("/auth/login",
                                 data={"username": user_data["email"], "password": user_data["password"]})

    # Проверяем, что статус код 200
    assert response.status_code == 200, f"Login failed: {response.text}"

    # Проверяем, что в ответе есть токен
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_protected_endpoint(client: AsyncClient, auth: dict):
    """
    Тест доступа к защищенному эндпоинту.
    """
    # Получаем токен из фикстуры auth
    token = auth["access_token"]

    # Делаем запрос к защищенному эндпоинту с токеном
    response = await client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    # Проверяем, что статус код 200
    assert response.status_code == 200

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
    await client.post("/users/", json=user_data)

    # Аутентификация и получение токена
    response = await client.post("/login", data={"username": user_data["email"], "password": user_data["password"]})

    assert response.status_code == 200, f"Authentication failed: {response.text}"
    return response.json()  # Токен будет в ответе, например, response.json()["access_token"]


@pytest.mark.asyncio
async def test(client: AsyncClient):
    """
    Тест для проверки GET-запроса на корневой URL.
    """
    response = await client.get("/users/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, user_data: dict):
    """
    Тест для создания пользователя через POST-запрос.
    """
    response = await client.post("/users/", json=user_data)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_existing_user(client: AsyncClient, user_data: dict):
    """
    Тест для создания пользователя через POST-запрос.
    """
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_read_users(client: AsyncClient):
    response = await client.get("/users/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_user(client: AsyncClient, user_data: dict, auth: dict):
    headers = {"Authorization": f"Bearer {auth['access_token']}"}
    me = await client.get("/users/me/", headers=headers)
    user_id = me.json()['user_id']
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, user_data: dict, auth: dict):
    headers = {"Authorization": f"Bearer {auth['access_token']}"}
    me = await client.get("/users/me/", headers=headers)
    user_id = me.json()['user_id']
    user_data["name"] = "newtest_user"
    print(user_data)
    response = await client.put(f"/users/{user_id}", headers=headers, json=user_data)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, user_data: dict, auth: dict):
    """
    Тест для удаления пользователя через DELETE-запрос с авторизацией.
    """
    headers = {"Authorization": f"Bearer {auth['access_token']}"}
    me = await client.get("/users/me/", headers=headers)
    user_id = me.json()['user_id']


    # Отправка запроса на удаление с авторизацией
    response = await client.delete(f"/users/{user_id}", headers=headers)
    assert response.status_code == 204

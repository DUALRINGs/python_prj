import pytest
from httpx import AsyncClient


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
    response = await client.post("/auth/login", data={"username": user_data["email"], "password": user_data["password"]})

    # Проверяем, что статус код 200
    assert response.status_code == 200, f"Login failed: {response.text}"

    # Проверяем, что в ответе есть токен
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_protected_endpoint(client: AsyncClient, token: str):
    """
    Тест доступа к защищенному эндпоинту.
    """
    # Получаем токен из фикстуры auth

    # Делаем запрос к защищенному эндпоинту с токеном
    response = await client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    # Проверяем, что статус код 200
    assert response.status_code == 200

import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from app.users.schemas import UserCreate
from app.main import app  # Импортируем ваше FastAPI-приложение
from app.auth.schemas import TokenInfo


# Фикстура для тестового клиента
@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# Фикстура для тестового пользователя
@pytest.fixture(scope="function")
async def test_user(client: AsyncClient):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret",
    }
    # Регистрируем пользователя (если у вас есть эндпоинт для регистрации)
    response = await client.post("/users", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user: dict):
    """
    Тест аутентификации пользователя и получения JWT-токена.
    """
    # Данные для входа
    login_data = {
        "username": test_user["email"],  # Используем email для входа
        "password": test_user["password"],
    }
    # Отправляем POST-запрос на /login
    response = await client.post("/login", data=login_data)
    # Проверяем, что ответ успешный
    assert response.status_code == 200
    # Проверяем, что в ответе есть токен
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_access_protected_endpoint(client: AsyncClient, test_user: dict):
    """
    Тест доступа к защищенному эндпоинту /users/me/ с использованием JWT-токена.
    """
    # Сначала аутентифицируемся
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    login_response = await client.post("/login", data=login_data)
    token = login_response.json()["access_token"]

    # Пытаемся получить доступ к защищенному эндпоинту
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/users/me/", headers=headers)
    # Проверяем, что ответ успешный
    assert response.status_code == 200
    # Проверяем, что в ответе есть информация о пользователе
    assert response.json()["email"] == test_user["email"]
    assert response.json()["username"] == test_user["username"]


@pytest.mark.asyncio
async def test_access_protected_endpoint_without_token(client: AsyncClient):
    """
    Тест доступа к защищенному эндпоинту /users/me/ без токена.
    """
    response = await client.get("/users/me/")
    # Проверяем, что доступ запрещен
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_login_with_wrong_password(client: AsyncClient, test_user: dict):
    """
    Тест аутентификации с неправильным паролем.
    """
    login_data = {
        "username": test_user["email"],
        "password": "wrong_password",  # Неправильный пароль
    }
    response = await client.post("/login", data=login_data)
    # Проверяем, что доступ запрещен
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
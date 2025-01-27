import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import helper
from app.users.schemas import UserUpdatePartial, User
from app.auth.utils import hash_password
from app.users.crud import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user
)

# Фикстура для сессии базы данных
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    # Создаем новую сессию
    async with helper.session_factory() as session:
        # Начинаем транзакцию
        await session.begin()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    user_in = User(
        name="testuser",
        email="test@example.com",
        password="password123"
    )
    # Проверяем создание нового пользователя
    created_user = await create_user(db_session, user_in)
    assert created_user.id is not None
    assert created_user.name == "testuser"
    assert created_user.email == "test@example.com"
    # Проверяем хэширование пароля
    assert validate_password("password123", created_user.password)

    # Проверяем, что пользователь не существует дважды
    with pytest.raises(HTTPException):
        await create_user(db_session, user_in)

@pytest.mark.asyncio
async def test_get_users_empty(db_session: AsyncSession):
    users = await get_users(db_session)
    assert users == []

@pytest.mark.asyncio
async def test_get_users_with_data(db_session: AsyncSession):
    user1 = User(
        name="user1",
        email="user1@example.com",
        password=hash_password("pass1")
    )
    user2 = User(
        name="user2",
        email="user2@example.com",
        password=hash_password("pass2")
    )
    db_session.add_all([user1, user2])
    await db_session.commit()

    users = await get_users(db_session)
    assert len(users) == 2
    # Проверяем сортировку по ID
    assert users[0].id < users[1].id

@pytest.mark.asyncio
async def test_get_user_exists(db_session: AsyncSession):
    user = User(
        name="testuser",
        email="test@example.com",
        password=hash_password("pass")
    )
    db_session.add(user)
    await db_session.commit()

    fetched_user = await get_user(db_session, user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id
    assert fetched_user.name == user.name

@pytest.mark.asyncio
async def test_get_user_not_found(db_session: AsyncSession):
    fetched_user = await get_user(db_session, 999)
    assert fetched_user is None

@pytest.mark.asyncio
async def test_update_user_full(db_session: AsyncSession):
    user = User(
        name="olduser",
        email="old@example.com",
        password=hash_password("oldpass")
    )
    db_session.add(user)
    await db_session.commit()

    update_data = UserUpdatePartial(
        name="newuser",
        email="new@example.com"
    )
    updated_user = await update_user(db_session, user, update_data, partial=False)

    assert updated_user.name == "newuser"
    assert updated_user.email == "new@example.com"
    assert validate_password("oldpass", updated_user.password)

    db_user = await get_user(db_session, user.id)
    assert db_user.name == "newuser"

@pytest.mark.asyncio
async def test_update_user_partial(db_session: AsyncSession):
    user = User(
        name="user",
        email="user@example.com",
        password=hash_password("pass")
    )
    db_session.add(user)
    await db_session.commit()

    update_data = UserUpdatePartial(email="newemail@example.com")
    updated_user = await update_user(db_session, user, update_data, partial=True)

    assert updated_user.email == "newemail@example.com"
    assert updated_user.name == "user"  # Неизмененное поле

@pytest.mark.asyncio
async def test_delete_user(db_session: AsyncSession):
    user = User(
        name="delete_me",
        email="delete@example.com",
        password=hash_password("pass")
    )
    db_session.add(user)
    await db_session.commit()

    await delete_user(db_session, user)

    deleted_user = await get_user(db_session, user.id)
    assert deleted_user is None

@pytest.mark.asyncio
async def test_delete_user_not_found(db_session: AsyncSession):
    user = User(
        name="delete_me",
        email="delete@example.com",
        password=hash_password("pass")
    )
    await delete_user(db_session, user)

    deleted_user = await get_user(db_session, user.id)
    assert deleted_user is None

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user_by_admin(client: AsyncClient, admin_token: str):
    response = await client.get(
    "/users/1",
    headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_user_by_admin(client: AsyncClient, user_data: dict, admin_token: str):
    user_data = {
        "name": "test_user_new",
        "password": "user_password",
        "email": "new_user@example.com",
        "is_active": True,
        "is_superuser": True,
        "is_verified": True
    }
    response = await client.patch(
    "/users/1",
    headers={"Authorization": f"Bearer {admin_token}"},
    json=user_data
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_user_by_admin(client: AsyncClient, admin_token: str):
    response = await client.delete(
        "/users/1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204
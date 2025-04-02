import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, task_data: dict, token: str):
    response = await client.post(
    "/tasks/",
    headers={"Authorization": f"Bearer {token}"},
    json=task_data,
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_read_tasks(client: AsyncClient, task_data: dict, token: str):
    response = await client.get(
    "/tasks/",
    headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_read_task_by_id(client: AsyncClient, task_data: dict, token: str):
    response = await client.get(
    "/tasks/1",
    headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_task_by_id(client: AsyncClient, task_data: dict, token: str):
    task_data["description"] = "updated description"
    response = await client.patch(
    "/tasks/1",
    headers={"Authorization": f"Bearer {token}"},
    json=task_data,
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_task_by_id(client: AsyncClient, task_data: dict, token: str):
    response = await client.delete(
    "/tasks/1",
    headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

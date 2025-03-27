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
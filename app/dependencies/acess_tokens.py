from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import Depends

from app.models import (
    helper,
    AccessToken,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_tokens_db(
    session: Annotated[
        "AsyncSession",
        Depends(helper.session_getter),
    ],
):
    yield AccessToken.get_db(session=session)
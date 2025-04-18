"""JWT бэкенд аутентификации для FastAPI Users с bearer-транспортом."""

from fastapi_users.authentication import AuthenticationBackend
from dependencies.authentication.transport import bearer_transport
from .strategy import get_jwt_strategy


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

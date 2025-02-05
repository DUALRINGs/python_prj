from authlib.oauth2.rfc6749.authenticate_client import authenticate_none
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from app.auth.transport import bearer_transport
from .strategy import get_jwt_strategy

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
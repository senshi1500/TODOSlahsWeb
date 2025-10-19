import uuid
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlmodel import SQLModelUserDatabase

from app.config import settings
from app.models import User
from app.db import get_async_session

# El BearerTransport define cómo se envía el token (en el encabezado Authorization: Bearer ...)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Clase para gestionar la lógica de negocio del usuario (creación, validación, etc.)
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.AUTH_SECRET
    verification_token_secret = settings.AUTH_SECRET

    # Aquí podrías añadir lógica personalizada para eventos (p. ej., enviar email tras registro)
    pass

# Función para obtener la instancia del UserManager
# primero: get_user_db
async def get_user_db(session: AsyncGenerator = Depends(get_async_session)):
    yield SQLModelUserDatabase(session, User)

# después: get_user_manager puede usar Depends(get_user_db)
async def get_user_manager(user_db: SQLModelUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

# Función para obtener el objeto SQLAlchemyUserDatabase que usa el User model
async def get_user_db(session: AsyncGenerator = Depends(get_async_session)):
    yield SQLModelUserDatabase(session, User)

# Estrategia de JWT: cómo se codifican y decodifican los tokens
def get_jwt_strategy() -> JWTStrategy:
    # lifetime_seconds: Define por cuánto tiempo es válido el token (p. ej., 3600 segundos = 1 hora)
    return JWTStrategy(secret=settings.AUTH_SECRET, lifetime_seconds=3600)

# Backend de Autenticación: combina el transporte y la estrategia
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Instancia principal de FastAPIUsers
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# Dependencia para proteger rutas: requiere que el usuario esté activo
current_active_user = fastapi_users.current_user(active=True)
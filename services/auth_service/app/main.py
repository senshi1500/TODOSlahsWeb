from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Depends
from fasthtml.common import FastHTML # Importación para la vista temporal

from app.db import create_db_and_tables
from app.config import settings
from app.users import fastapi_users, auth_backend, current_active_user
from app.schemas import UserRead, UserCreate, UserUpdate

# 💡 Función que se ejecuta al iniciar/finalizar la aplicación (ASGI lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al inicio: Crea las tablas de la base de datos si no existen
    await create_db_and_tables()
    yield
    # Al finalizar: Limpieza (opcional)

app = FastAPI(
    title="Auth Microservice",
    version="0.1.0",
    lifespan=lifespan # Conecta la función de ciclo de vida
)

# ------------------------------------------------
# 1. Rutas de Autenticación de fastapi-users
# ------------------------------------------------

# Ruta de Login/Logout (usa la estrategia JWT)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Ruta de Registro
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Rutas de Gestión de Usuario (obtener/actualizar/borrar usuario por ID)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Ruta protegida de ejemplo (requiere usuario logueado)
@app.get("/authenticated-route", tags=["users"])
async def authenticated_route(user: UserRead = Depends(current_active_user)) -> Dict[str, Any]:
    return {"message": f"Hello {user.email}! You are authenticated."}


# ------------------------------------------------
# 2. Rutas de Frontend Temporal (FastHTML) - Si está habilitado
# ------------------------------------------------

if settings.FASTHTML_ENABLED:
    # Creamos una instancia básica de FastHTML para renderizar el frontend
    html_app = FastHTML()
    
    # Ruta temporal de inicio para el frontend
    @html_app.get("/")
    def home():
        # En una aplicación real con FastHTML, aquí se renderizaría HTML
        return {"message": "FastHTML está habilitado. ¡Aquí iría tu frontend temporal!"}

    app.mount("/client", html_app) # Montamos el frontend temporal bajo /client
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# 💡 Lógica para seleccionar la URL de la DB
if settings.MODE == "DEV_DOCKER":
    db_url = settings.AUTH_DATABASE_URL_DOCKER # Asegúrate de haber definido esto en config.py
elif settings.MODE == "DEV_LOCAL":
    db_url = settings.AUTH_DATABASE_URL_LOCAL # Asegúrate de haber definido esto en config.py
else:
    raise ValueError(f"Modo de desarrollo desconocido: {settings.MODE}")

# Crea el motor de la base de datos usando la URL seleccionada
engine = create_async_engine(db_url, echo=True)

async def create_db_and_tables():
    """Crea la base de datos y las tablas si no existen."""
    async with engine.begin() as conn:
        # Crea la tabla de la base de datos basada en los modelos SQLModel/fastapi-users
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Inyecta la sesión de la base de datos en las rutas (Dependency Injection)."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
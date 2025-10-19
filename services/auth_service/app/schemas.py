import uuid
from fastapi_users import schemas
from typing import Optional

# 💡 Esquema para la lectura de datos de usuario (lo que devuelve la API)
# Se usa para mostrar el perfil del usuario después del login/registro.
class UserRead(schemas.BaseUser[uuid.UUID]):
    full_name: Optional[str] = None
    pass

# 💡 Esquema para el registro de un nuevo usuario (lo que se espera en el POST /auth/register)
class UserCreate(schemas.BaseUserCreate):
    full_name: Optional[str] = None
    pass

# 💡 Esquema para la actualización de un usuario (PATCH /users/{user_id})
class UserUpdate(schemas.BaseUserUpdate):
    # 💡 Esquema para la lectura de datos de usuario (lo que devuelve la API)
    # Se usa para mostrar el perfil del usuario después del login/registro.
    class UserRead(schemas.BaseUser[uuid.UUID]):
        full_name: Optional[str] = None
        pass

    # 💡 Esquema para el registro de un nuevo usuario (lo que se espera en el POST /auth/register)
    class UserCreate(schemas.BaseUserCreate):
        full_name: Optional[str] = None
        pass

    # 💡 Esquema para la actualización de un usuario (PATCH /users/{user_id})
    class UserUpdate(schemas.BaseUserUpdate):
        full_name: Optional[str] = None
        pass
    pass
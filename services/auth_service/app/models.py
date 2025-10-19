from typing import Optional
from sqlmodel import Field
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
# SQLAlchemyBaseUserTableUUID incluye campos de usuario estándar y usa UUIDs como PK

# 💡 El modelo base de usuario para la base de datos (lo que se almacena en la tabla)
class User(SQLModelBaseUserDB, table=True):
    # Puedes añadir campos personalizados aquí. 
    # Por ejemplo, un campo de nombre completo:
    full_name: Optional[str] = Field(default=None, max_length=100)
    
    # Los campos estándar (email, hashed_password, is_active, is_superuser, is_verified)
    # ya están incluidos al heredar de SQLAlchemyBaseUserTableUUID
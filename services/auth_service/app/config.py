# app/config.py
from pathlib import Path  # Importamos Pathlib para el manejo de rutas
from pydantic_settings import BaseSettings, SettingsConfigDict

# Esto obtiene la ruta del archivo config.py (el archivo actual).
CURRENT_FILE_PATH = Path(__file__).resolve()

# Nos movemos tres niveles hacia arriba para llegar a la raíz del proyecto.
# config.py -> app/ -> auth-microservice/ -> project-root/
ENV_FILE_PATH = CURRENT_FILE_PATH.parent.parent.parent.parent / ".env"

class Settings(BaseSettings):
    
    # Modo y Front-end
    MODE: str = "DEV_LOCAL" 
    FASTHTML_ENABLED: bool = True
    AUTH_PORT: int = 8000
    
    # Secreto de Autenticación
    AUTH_SECRET: str
    
    # URLs de Conexión, basadas en el modo
    AUTH_DATABASE_URL_LOCAL: str
    AUTH_DATABASE_URL_DOCKER: str

    # Variable que se resolverá en el código (no se define en el .env)
    @property
    def DATABASE_URL(self) -> str:
        if self.MODE == "DEV_DOCKER":
            return self.AUTH_DATABASE_URL_DOCKER
        return self.AUTH_DATABASE_URL_LOCAL # Por defecto, usa DEV_LOCAL
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, # Usamos la ruta absoluta calculada
        extra='ignore'
    )

settings = Settings()
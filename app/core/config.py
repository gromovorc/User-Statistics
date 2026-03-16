from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

SECRET_KEY = "b4cb3b761c84ee0d18780a36eb39144dc0816e288f26997206c42366f9f5b1f9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings(BaseSettings):
    app_name: str
    debug: bool
    database_url: str

    model_config = SettingsConfigDict(
        env_file= ENV_PATH
    )

settings = Settings()
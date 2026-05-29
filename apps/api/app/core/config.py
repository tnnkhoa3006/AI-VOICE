from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

  app_env: str = "development"
  app_name: str = "MiMo Voice Studio API"
  frontend_url: str = "http://localhost:3000"
  api_public_url: str = "http://localhost:8000"

  database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/mimo_voice_studio"
  redis_url: str = "redis://localhost:6379/0"

  auth_dev_bypass: bool = True
  dev_user_email: str = "demo@mimostudio.local"
  supabase_jwt_secret: str | None = None

  mimo_api_key: str = "dev-placeholder"
  mimo_tts_url: str | None = None

  storage_backend: str = "local"
  local_storage_path: str = "storage"
  r2_account_id: str | None = None
  r2_access_key_id: str | None = None
  r2_secret_access_key: str | None = None
  r2_bucket_name: str | None = None

  auto_create_tables: bool = True

  @computed_field
  @property
  def cors_origins(self) -> list[str]:
    return [origin.strip() for origin in self.frontend_url.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
  return Settings()


settings = get_settings()


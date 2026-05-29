from pathlib import Path

from app.core.config import settings


class StorageService:
  def save_audio(self, storage_key: str, content: bytes, content_type: str) -> str:
    if settings.storage_backend != "local":
      raise NotImplementedError("R2/S3 storage is not wired yet")

    root = Path(settings.local_storage_path)
    path = root / storage_key
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    safe_key = storage_key.replace("\\", "/")
    return f"{settings.api_public_url}/media/{safe_key}"

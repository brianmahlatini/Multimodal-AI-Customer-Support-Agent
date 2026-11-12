from pathlib import Path

from app.core.config import settings


class ObjectStorage:
    def save_bytes(self, key: str, content: bytes) -> str:
        path = Path(settings.local_object_store) / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return f"local://{path.as_posix()}"

from __future__ import annotations
import shutil
from pathlib import Path
from typing import BinaryIO
from storage.storage_provider import StorageProvider

class LocalStorageProvider(StorageProvider):

    def __init__(self, root: str | Path = "storage") -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def store(self, *, file: BinaryIO, path: str, content_type: str | None = None) -> str:
        target = self._safe_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)

        with target.open("wb") as destination:
            shutil.copyfileobj(file, destination)

        return self._relative_path(target)

    def open(self, *, path: str) -> BinaryIO:
        target = self._safe_path(path)

        if not target.exists():
            raise FileNotFoundError(path)

        if not target.is_file():
            raise IsADirectoryError(path)

        return target.open("rb")

    def delete(self, *, path: str) -> None:
        target = self._safe_path(path)

        if target.exists():
            if not target.is_file():
                raise IsADirectoryError(path)

            target.unlink()

    def exists(self, *, path: str) -> bool:
        return self._safe_path(path).is_file()

    def size(self, *, path: str) -> int:
        target = self._safe_path(path)

        if not target.exists():
            return 0

        if not target.is_file():
            raise IsADirectoryError(path)

        return target.stat().st_size

    def url(self, *, path: str, expires_in: int = 3600) -> str:

        return str(self._safe_path(path))

    def move(self, *, source: str, destination: str) -> str:
        source_path = self._safe_path(source)
        destination_path = self._safe_path(destination)

        if not source_path.exists():
            raise FileNotFoundError(source)

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(source_path), str(destination_path))

        return self._relative_path(destination_path)

    def copy(self, *, source: str, destination: str) -> str:
        source_path = self._safe_path(source)
        destination_path = self._safe_path(destination)

        if not source_path.exists():
            raise FileNotFoundError(source)

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source_path, destination_path)

        return self._relative_path(destination_path)

    def _safe_path(self, path: str) -> Path:
        candidate = (self.root / path).resolve()

        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("Storage path escapes the storage root.") from exc

        return candidate

    def _relative_path(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()
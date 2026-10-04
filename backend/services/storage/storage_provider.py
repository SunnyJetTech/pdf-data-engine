from __future__ import annotations
from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageProvider(ABC):
    @abstractmethod
    def store( self, *, file: BinaryIO, path: str, content_type: str | None = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def open(self, *, path: str) -> BinaryIO: 
        raise NotImplementedError

    @abstractmethod
    def delete(self, *, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, *, path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def size(self, *, path: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def url(self, *, path: str, expires_in: int = 3600) -> str:
        raise NotImplementedError

    @abstractmethod
    def move(self, *, source: str, destination: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def copy(self, *, source: str, destination: str) -> str:
        raise NotImplementedError
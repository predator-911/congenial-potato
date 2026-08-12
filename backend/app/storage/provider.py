from abc import ABC, abstractmethod
from pathlib import Path


class StorageProvider(ABC):
    @abstractmethod
    def object_path(self, storage_filename: str) -> Path: ...
    @abstractmethod
    def delete(self, storage_filename: str) -> None: ...
    @abstractmethod
    def exists(self, storage_filename: str) -> bool: ...

from abc import ABC, abstractmethod
from typing import Iterable
from pathlib import Path
import json


class FileLoader(ABC):
    """Base class for loading files"""

    @abstractmethod
    def load(self, files: Iterable[Path]) -> Iterable[dict]:
        """Load the files"""


class JSONFileLoader(FileLoader):
    """Load json files"""

    def load(self, files: Iterable[Path]) -> Iterable[dict]:
        data = []
        for path in files:
            with open(path, encoding="utf-8") as data_file:
                data.append(json.load(data_file, strict=False))
        return data


class FileSearcher(ABC):
    """Base class for searching for files"""

    @abstractmethod
    def search(self, path: Path) -> Iterable[Path]:
        """Nice"""


class GlobFileSearcher(FileSearcher):
    """Search for files via glob patterns"""

    def __init__(self, glob: str) -> None:
        super().__init__()
        self._glob = glob

    def search(self, path: Path) -> Iterable[Path]:
        return path.glob(self._glob)

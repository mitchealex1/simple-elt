"""Handle the requests"""

from __future__ import annotations
from pathlib import Path
from sqlalchemy import MetaData, Engine, URL, create_engine
from datasets import Dataset
from actions import Action


class ConfigValidationError(Exception):
    """An error related to validation of the config"""

    def __init__(self, message: str) -> None:
        self._message = message

    def __str__(self) -> str:
        return f"Error validating the config: {self._message}"


class Backend:
    """Handle requests"""

    def __init__(self, config: dict) -> None:
        self._config = config
        self._metadata = None
        self._engine = None
        self._data_directory = None

    def _setup(self) -> Backend:
        url = URL.create(
            drivername="postgresql",
            username=self._config["postgres_user"],
            password=self._config["postgres_password"],
            host=self._config["postgres_host"],
            port=self._config["postgres_port"],
            database=self._config["postgres_database"],
        )
        metadata = MetaData(schema=self._config["postgres_schema"])
        engine = create_engine(url)
        self._metadata = metadata
        self._engine = engine
        self._data_directory = self._config["data_directory"]
        return self

    @property
    def engine(self) -> Engine:
        """Lazy load the engine object"""
        if not self._engine:
            self._setup()
        return self._engine

    @property
    def metadata(self) -> MetaData:
        """Lazy load the metadata object"""
        if not self._metadata:
            self._setup()
        return self._metadata

    @property
    def data_directory(self) -> Path:
        """Lazy load the data_directory path"""
        if not self._data_directory:
            self._setup()
        return self._data_directory

    def execute(self, dataset_input: str, action_input: str) -> None:
        """Execute an action for a dataset"""
        dataset = Dataset.from_string(dataset_input).init(self.data_directory)
        action = Action.from_string(action_input).init(self.metadata, self.engine)
        dataset.execute(action)

"""The possible actions that can be executed for a dataset"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import Table, Column, JSON, DateTime, MetaData, Engine


if TYPE_CHECKING:
    from datasets import GenericDataset, WrapperDataset


class Action(ABC):
    """An action that can be executed for a dataset"""

    def __init__(self) -> None:
        super().__init__()
        self._metadata = None
        self._engine = None

    def init(self, metadata: MetaData, engine: Engine) -> Action:
        """Init the action"""
        self._metadata = metadata
        self._engine = engine
        return self

    @classmethod
    def from_string(cls: Action, string: str):
        """Create an action from a string"""
        if string.lower() == "load":
            return Load()
        if string.lower() == "unload":
            return Unload()
        raise NotImplementedError(f"Statement {string} not implemented")

    def _get_table(self, dataset_name: str) -> Table:
        return Table(
            dataset_name,
            self._metadata,
            Column("file_content", JSON),
            Column("load_timestamp", DateTime(timezone=True)),
        )

    @abstractmethod
    def execute_for_wrapper_dataset(self, wrapper_dataset: WrapperDataset) -> None:
        """Execute the action for each dataset in a dataset wrapper"""

    @abstractmethod
    def execute_for_generic_dataset(self, generic_dataset: GenericDataset) -> None:
        """Execute the action for a dataset"""


class Load(Action):
    """Load the data for a dataset"""

    def execute_for_generic_dataset(self, generic_dataset: GenericDataset) -> None:
        table = self._get_table(generic_dataset.name)
        table.create(self._engine, checkfirst=True)
        with self._engine.connect() as connection:
            connection.execute(table.delete())
            connection.commit()
        load_timestamp = datetime.now(tz=timezone.utc)
        table_data = [
            {"file_content": datum, "load_timestamp": load_timestamp}
            for datum in generic_dataset.data
        ]
        with self._engine.connect() as connection:
            connection.execute(table.insert().values(table_data))
            connection.commit()

    def execute_for_wrapper_dataset(self, wrapper_dataset: WrapperDataset) -> None:
        for dataset in wrapper_dataset.datasets:
            dataset.execute(self)


class Unload(Action):
    """Unload the data for a dataset"""

    def execute_for_generic_dataset(self, generic_dataset: GenericDataset) -> None:
        table = self._get_table(generic_dataset.name)
        table.drop(self._engine, checkfirst=True)

    def execute_for_wrapper_dataset(self, wrapper_dataset: WrapperDataset) -> None:
        for dataset in wrapper_dataset.datasets:
            dataset.execute(self)

"""Objects encapsulate the facebook datasets"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable
from pathlib import Path
from files import JSONFileLoader, FileLoader, GlobFileSearcher, FileSearcher

if TYPE_CHECKING:
    from actions import Action


class Dataset(ABC):
    """Base class to encapsulate a dataset"""

    def __init__(self, name: str) -> None:
        self._name = name
        self._data_directory = None
        super().__init__()

    @property
    def name(self) -> str:
        """The name of the dataset"""
        return self._name

    def init(self, data_directory: Path) -> Dataset:
        """Init the dataset"""
        self._data_directory = data_directory
        return self

    @classmethod
    def from_string(cls: Dataset, string: str):
        """Create a dataset from a string"""
        if string.lower() == "messages":
            return WrapperDataset(
                "messages",
                {
                    GenericDataset(
                        "messages_inbox",
                        JSONFileLoader(),
                        GlobFileSearcher("*/messages/inbox/*/*.json"),
                    ),
                    GenericDataset(
                        "messages_archived_threads",
                        JSONFileLoader(),
                        GlobFileSearcher("*/messages/archived_threads/*/*.json"),
                    ),
                    GenericDataset(
                        "messages_filtered_threads",
                        JSONFileLoader(),
                        GlobFileSearcher("*/messages/filtered_threads/*/*.json"),
                    ),
                    GenericDataset(
                        "messages_message_requests",
                        JSONFileLoader(),
                        GlobFileSearcher("*/messages/message_requests/*/*.json"),
                    ),
                },
            )
        if string.lower() == "friends_and_followers":
            return WrapperDataset(
                "friends_and_followers",
                {
                    GenericDataset(
                        "friends_and_followers_friends",
                        JSONFileLoader(),
                        GlobFileSearcher("*/friends_and_followers/friends.json"),
                    ),
                    GenericDataset(
                        "friends_and_followers_friend_requests_received",
                        JSONFileLoader(),
                        GlobFileSearcher(
                            "*/friends_and_followers/friend_requests_received.json"
                        ),
                    ),
                    GenericDataset(
                        "friends_and_followers_friend_requests_sent",
                        JSONFileLoader(),
                        GlobFileSearcher(
                            "*/friends_and_followers/friend_requests_sent.json"
                        ),
                    ),
                },
            )
        raise NotImplementedError(f"Dataset {string} not implemented")

    @abstractmethod
    def execute(self, action: Action):
        """Execute an action for a dataset"""


class WrapperDataset(Dataset):
    """A dataset that contains multiple datasets"""

    def __init__(self, name: str, datasets: Iterable[Dataset]) -> None:
        self._datasets = datasets
        super().__init__(name)

    @property
    def datasets(self) -> Iterable[Dataset]:
        """The datasets"""
        return self._datasets

    def execute(self, action: Action):
        action.execute_for_wrapper_dataset(self)

    def init(self, data_directory: Path) -> Dataset:
        super().init(data_directory)
        for dataset in self.datasets:
            dataset.init(data_directory)
        return self


class GenericDataset(Dataset):
    """A simple dataset"""

    def __init__(
        self, name: str, file_loader: FileLoader, file_searcher: FileSearcher
    ) -> None:
        self._file_loader = file_loader
        self._file_searcher = file_searcher
        super().__init__(name)

    @property
    def data(self):
        """The data within the dataset"""
        return self._file_loader.load(self._file_searcher.search(self._data_directory))

    def execute(self, action: Action):
        action.execute_for_generic_dataset(self)

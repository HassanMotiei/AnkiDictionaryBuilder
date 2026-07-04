from abc import ABC, abstractmethod

from ankidict.core.models import DictionaryEntry


class BaseRepository(ABC):

    @abstractmethod
    def save(self, entry: DictionaryEntry):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass
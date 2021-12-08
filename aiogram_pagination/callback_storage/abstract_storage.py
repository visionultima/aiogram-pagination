from abc import ABC, abstractmethod

from ..utils.singlton import AbstractSingleton


class AbstractCallbackStorage(ABC, metaclass=AbstractSingleton):

    @abstractmethod
    def add_callback(self, callback: str):
        pass

    @abstractmethod
    def remove_callback(self, callback: str):
        pass

    @abstractmethod
    def clear(self):
        pass

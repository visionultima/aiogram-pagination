from abc import abstractmethod

from aiogram_pagination.utils.misc.singlton import AbstractSingleton


class BaseCallbackStorage(metaclass=AbstractSingleton):

    @abstractmethod
    def add_callback(self, callback: str):
        pass

    @abstractmethod
    def remove_callback(self, callback: str):
        pass

    @abstractmethod
    def get_callback(self, abbreviation) -> str:
        pass

    @abstractmethod
    def get_abbreviation(self, callback):
        pass

    @abstractmethod
    def on_callbacks_exceeding_time_limit(self, cache_time_limit):
        pass

    @abstractmethod
    def clear(self):
        pass

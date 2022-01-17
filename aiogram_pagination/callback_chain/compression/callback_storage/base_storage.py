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
    def clear(self):
        pass

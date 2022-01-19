from abc import ABCMeta, abstractmethod


class BaseCallbackChain(metaclass=ABCMeta):
    @abstractmethod
    def next(self, new_current_callback_query: str) -> str:
        pass

    @abstractmethod
    def edit_current_callback_query(self, new_current_callback_query: str) -> str:
        pass

    @abstractmethod
    def previous(self) -> str:
        pass

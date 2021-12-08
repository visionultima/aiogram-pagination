from abc import ABC, abstractmethod

from ..utils.callback_stack_factory import CallbackStackFactory


class AbstractCallbackStack(ABC):
    @abstractmethod
    def next(self, callback_data: dict, callback_factory: CallbackStackFactory) -> str:
        pass

    @abstractmethod
    def edit_callback_data(self, callback_data: dict, callback_factory: CallbackStackFactory) -> str:
        pass

    @abstractmethod
    def previous(self) -> str:
        pass

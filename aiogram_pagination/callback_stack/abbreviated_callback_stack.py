from .abstract_callback_stack import AbstractCallbackStack
from .callback_stack import CallbackStack
from ..utils.callback_stack_factory import CallbackStackFactory
from ..data.loader import configurator


class AbbreviatedCallbackStack(AbstractCallbackStack):

    def __init__(self, callback_data: dict, callback_factory: CallbackStackFactory):
        self.callback_stack = CallbackStack(callback_data, callback_factory)
        self.previous_callback_data = self.callback_stack.generate_previous_callback_data()
        self.configurator = configurator
        self.config = self.configurator.config
        self.callback_storage = self.configurator.get_storage(self.config)

    def next(self, callback_data: dict, callback_factory: CallbackStackFactory) -> str:
        previous_callback_data = self.previous_callback_data.copy()
        old_callback_data = self.callback_stack.get_string_callback_data()
        self.callback_storage.add_callback(old_callback_data)
        self.push(previous_callback_data, old_callback_data)

        return self.callback_stack.get_complete_string_callback_data(
            callback_data, callback_factory, previous_callback_data
        )

    def edit_callback_data(self, callback_data: dict, callback_factory: CallbackStackFactory) -> str:
        return self.callback_stack.get_complete_string_callback_data(
            callback_data, callback_factory, self.previous_callback_data
        )

    def previous(self, default: str = str()) -> str:
        previous_callback_data = self.previous_callback_data.copy()
        callback_data = self.pop(previous_callback_data) or default
        self.callback_storage.remove_callback(callback_data)
        return f'{callback_data}{self.callback_stack.get_string_previous_callback_data(previous_callback_data)}'

    def push(self, previous_callback_data: list, callback_data: str) -> None:
        excess = len(previous_callback_data) - (self.config.max_pagination_depth or float('inf'))
        if excess > 0:
            previous_callback_data = previous_callback_data[excess + 1:]
        previous_callback_data.append(str(self.callback_storage.get_abbreviation(callback_data)))

    def pop(self, previous_callback_data: list) -> str:
        return self.callback_storage.get_callback(previous_callback_data.pop(-1))

from .abstract_callback_stack import AbstractCallbackStack
from .callback_stack import CallbackStackFactory, CallbackStack
from ..data.loader import configurator


class SimpleCallbackStack(AbstractCallbackStack):

    def __init__(self, callback_data: dict, callback_factory: CallbackStackFactory):
        self.configurator = configurator
        self.config = self.configurator.config
        self.callback_stack = CallbackStack(callback_data, callback_factory)
        self.previous_callback_data = self.callback_stack.generate_previous_callback_data()

    def next(self, callback_data: dict, callback_factory: CallbackStackFactory):
        previous_callback_data = self.previous_callback_data.copy()
        self.push(previous_callback_data, self.callback_stack.get_string_callback_data())
        return self.callback_stack.get_complete_string_callback_data(
            callback_data, callback_factory, previous_callback_data
        )

    def edit_callback_data(self, callback_data: dict, callback_factory: CallbackStackFactory) -> str:
        return self.callback_stack.get_complete_string_callback_data(
            callback_data, callback_factory, self.previous_callback_data
        )

    def previous(self) -> str:
        previous_callback_data = self.previous_callback_data.copy()
        callback_data = self.pop(previous_callback_data)
        return f'{callback_data}{self.callback_stack.get_string_previous_callback_data(previous_callback_data)}'

    def push(self, previous_callback_data: list, callback_data):
        excess = len(previous_callback_data) - (self.config.max_pagination_depth or float('inf'))
        if excess > 0:
            previous_callback_data = previous_callback_data[excess+1:]
        previous_callback_data.append(callback_data.replace(
            self.callback_stack.callback_factory.sep, '|')
        )

    def pop(self, previous_callback_data):
        return previous_callback_data.pop(-1).replace('|', self.callback_stack.callback_factory.sep)

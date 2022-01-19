from aiogram_pagination.callback_chain.callback import PreviousCallback
from aiogram_pagination.data.config import config


class CallbackStack:

    def __init__(self, callback: PreviousCallback):
        self.config = config
        self.callback = callback
        self.previous_callback_data = self.callback.previous_callback_data

    def push(self, callback_query: str):
        len_of_previous_callback_data = len(self.callback.get_previous_callback_data())
        excess = len_of_previous_callback_data - (self.config.max_pagination_depth or float('inf'))
        if excess > 0:
            self.previous_callback_data = self.previous_callback_data[excess+1:]
        self.previous_callback_data.append(callback_query)

    def pop(self) -> str:
        return self.previous_callback_data.pop()

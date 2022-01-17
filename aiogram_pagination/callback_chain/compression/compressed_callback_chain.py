from aiogram_pagination.callback_chain.base_callback_chain import BaseCallbackStack
from aiogram_pagination.callback_chain.callback_stack.callback_stack import CallbackStack, PreviousCallback
from aiogram_pagination.utils.callback_stack_factory import CallbackStackFactory
from aiogram_pagination.data.loader import configurator
from aiogram_pagination.data.loader import storages


class CompressedCallbackChain(BaseCallbackStack):

    def __init__(self, factory: CallbackStackFactory, query: str = None, data: dict = None):
        self.callback = PreviousCallback(factory, query, data)
        self.configurator = configurator
        self.config = self.configurator.config
        self.storage = storages.get_storage(self.config)
        self.callback_stack = CallbackStack(self.callback)

    def next(self, new_current_callback_query: str) -> str:
        old_current_callback_query = self.callback.get_current_callback_query()
        old_current_callback_query = old_current_callback_query
        self._compress(old_current_callback_query)
        self.callback_stack.push(self.storage.get_abbreviation(old_current_callback_query))
        return self.callback.validate_callback_query(
            new_current_callback_query, self.callback.get_previous_callback_queries()
        )

    def edit_current_callback_query(self, new_current_callback_query: str) -> str:
        return f'{new_current_callback_query}{self.callback.get_previous_callback_queries()}'

    def previous(self, default: str = '') -> str:
        new_current_callback_query = self._decompress() or default
        return f'{new_current_callback_query}{self.callback.get_previous_callback_queries()}'

    def _decompress(self):
        self.storage.remove_callback(decompressed := self.storage.get_callback(self.callback_stack.pop()))
        return decompressed

    def _compress(self, callback_query):
        self.storage.add_callback(callback_query)

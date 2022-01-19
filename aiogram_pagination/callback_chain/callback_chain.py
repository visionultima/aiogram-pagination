from aiogram_pagination.callback_chain.callback_stack.callback_stack import CallbackStack
from aiogram_pagination.callback_chain.base_callback_chain import BaseCallbackChain
from aiogram_pagination.utils.callback_stack_factory import CallbackStackFactory
from aiogram_pagination.callback_chain.callback import PreviousCallback


class CallbackChain(BaseCallbackChain):

    def __init__(self, factory: CallbackStackFactory, query: str = None, data: dict = None):
        self.callback = PreviousCallback(factory, query, data)
        self.callback_stack = CallbackStack(self.callback)

    def next(self, new_current_callback_query: str) -> str:
        old_current_callback_query = self.callback.get_current_callback_query()
        old_current_callback_query = old_current_callback_query.replace(':', '')
        self.callback_stack.push(old_current_callback_query)
        return self.callback.validate_callback_query(
            new_current_callback_query,
            self.callback.get_previous_callback_queries()
        )

    def edit_current_callback_query(self, new_current_callback_query: str) -> str:
        return f'{new_current_callback_query}{self.callback.get_previous_callback_queries()}'

    def previous(self) -> str:
        new_current_callback_query = self.callback_stack.pop().replace(self.callback.separator, ':')
        return f'{new_current_callback_query}{self.callback.get_previous_callback_queries()}'

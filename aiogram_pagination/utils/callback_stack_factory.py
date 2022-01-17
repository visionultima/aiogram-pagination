from aiogram.utils.callback_data import CallbackData

from aiogram_pagination.utils.misc.overloading import overload, OverloadMeta


class CallbackStackFactory(CallbackData, metaclass=OverloadMeta):
    def __init__(self, prefix, *parts):
        super().__init__(prefix, *parts)
        self._part_names = *self._part_names, 'previous'

    @overload
    def new(self, previous='', *args, **kwargs) -> str:
        return super().new(*args, **kwargs, previous=previous)

    @overload
    def new(self, *args, previous='', **kwargs) -> str:
        return super().new(*args, **kwargs, previous=previous)

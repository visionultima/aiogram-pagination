from aiogram.utils.callback_data import CallbackData


class CallbackStackFactory(CallbackData):
    def __init__(self, prefix, *parts):
        super().__init__(prefix, *parts)
        self._part_names = *self._part_names, 'previous'

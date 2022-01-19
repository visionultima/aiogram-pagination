from datetime import datetime

from aiogram_pagination.utils.compression.counter import Counter
from aiogram_pagination.utils.db_api.schemas import Callback
from .base_storage import BaseCallbackStorage


class SQLiteCallbackStorage(BaseCallbackStorage):

    def __init__(self):
        self._table = Callback
        self._table.create_table()
        self._counter = Counter()
        self._pointers = list()

    def add_callback(self, callback: str):
        callback_field = self._get_row_on_callback(callback)
        if not callback_field:
            abbreviation = self._pointers.pop() if len(self._pointers) > 0 else self._counter.count
            callback_field = self._table.create(callback=callback, abbreviation=abbreviation)
            self._counter.increment()
        callback_field.use_counter += 1

    def remove_callback(self, callback: str):
        removed_callback = self._get_row_on_callback(callback)
        if not removed_callback:
            return
        self._pointers.append(removed_callback.abbreviation)
        removed_callback.use_counter -= 1
        if removed_callback.use_counter == 0:
            removed_callback.delete_instance()

    def get_callback(self, abbreviation) -> str:
        return self._get_row_on_abbreviation(abbreviation).callback

    def get_abbreviation(self, callback):
        return self._get_row_on_callback(callback).abbreviation

    def _get_row_on_callback(self, callback: str) -> Callback:
        return self._table.get_or_none(self._table.callback == callback)

    def _get_row_on_abbreviation(self, abbreviation: str) -> Callback:
        return self._table.get_or_none(self._table.abbreviation == abbreviation)

    def on_callbacks_exceeding_time_limit(self, cache_time_limit: int):
        self._table.delete().where(
            datetime.now().timestamp() - self._table.updated_at.to_timestamp() > cache_time_limit
        )

    def clear(self):
        self._table.truncate_table()
        self._pointers = list()
        self._counter.nullify()

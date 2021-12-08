from datetime import datetime

from .abstract_storage import AbstractCallbackStorage
from ..utils.counter import Counter
from ..utils.db_api.schemas import Callback


class SQLiteCallbackStorage(AbstractCallbackStorage):

    def __init__(self):
        self.table = Callback
        self.table.create_table()
        self.counter = Counter()
        self.pointers = list()

    def add_callback(self, callback: str):
        callback_field = self._get_row_on_callback(callback)
        if not callback_field:
            abbreviation = self.pointers.pop() if len(self.pointers) > 0 else self.counter.count
            callback_field = self.table.create(callback=callback, abbreviation=abbreviation)
            self.counter.increment()
        callback_field.use_counter += 1

    def remove_callback(self, callback: str):
        removed_callback = self._get_row_on_callback(callback)
        if not removed_callback:
            return
        self.pointers.append(removed_callback.abbreviation)
        removed_callback.use_counter -= 1
        if removed_callback.use_counter == 0:
            removed_callback.delete_instance()

    def get_callback(self, abbreviation) -> str:
        return self._get_row_on_abbreviation(abbreviation).callback

    def get_abbreviation(self, callback):
        return self._get_row_on_callback(callback).abbreviation

    def _get_row_on_callback(self, callback: str) -> Callback:
        return self.table.get_or_none(self.table.callback == callback)

    def _get_row_on_abbreviation(self, abbreviation: str) -> Callback:
        return self.table.get_or_none(self.table.abbreviation == abbreviation)

    def on_callbacks_exceeding_time_limit(self, cache_time_limit: int):
        self.table.delete().where(
            datetime.now().timestamp() - self.table.updated_at.to_timestamp() > cache_time_limit
        )

    def clear(self):
        self.table.truncate_table()
        self.pointers = list()
        self.counter.nullify()

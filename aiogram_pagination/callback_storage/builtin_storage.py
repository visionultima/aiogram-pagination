from datetime import datetime

from .abstract_storage import AbstractCallbackStorage
from ..utils.counter import Counter


class BuiltinCallbackStorage(AbstractCallbackStorage):

    def __init__(self):
        self._storage = dict()
        self._counter = Counter()
        self._pointers = list()

    def add_callback(self, callback: str):
        if not self._check_callback_existing(callback):
            abbreviation = self._pointers.pop() if len(self._pointers) > 0 else self._counter.count
            self._storage[callback] = dict()
            self._storage[callback]['abbreviation'] = abbreviation
            self._storage[callback]['created_at'] = datetime.now()
            self._storage[callback]['updated_at'] = datetime.now()
            self._storage[callback]['use_counter'] = 1
            self._counter.increment()
        else:
            self._storage[callback]['updated_at'] = datetime.now()
            self._storage[callback]['use_counter'] += 1

    def remove_callback(self, callback: str):
        if self._check_callback_existing(callback):
            self._storage[callback]['use_counter'] -= 1
            if self._storage[callback]['use_counter'] <= 0:
                self._pointers.append(self._storage.pop(callback))

    def get_callback(self, abbreviation: str) -> str:
        for key, value in self._storage.items():
            if value['abbreviation'] == abbreviation:
                return key

    def get_abbreviation(self, callback: str) -> str:
        return self._storage.get(callback)['abbreviation']

    def _check_callback_existing(self, callback: str) -> bool:
        return callback in self._storage

    def on_callbacks_exceeding_time_limit(self, cache_time_limit: int):
        for callback in self._storage:
            callback_time = datetime.now().timestamp() - self._storage[callback]['updated_at'].timesatmp()
            if callback_time > cache_time_limit:
                self._pointers.append(self._storage.pop(callback))

    def clear(self):
        self._storage = dict()
        self._pointers = list()
        self._counter.nullify()

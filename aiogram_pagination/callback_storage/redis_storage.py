from datetime import datetime

from redis import Redis

from .abstract_storage import AbstractCallbackStorage
from ..data.loader import configurator
from ..utils.counter import Counter


class RedisCallbackStorage(AbstractCallbackStorage):

    def __init__(self):
        self._configurator = configurator
        self._config = self._configurator.config
        self._db = self._config.redis_db
        self._redis = Redis(db=self._db)
        self._counter = Counter()
        self._pointers = list()

    def add_callback(self, callback: str):
        if self._check_callback_existing(callback):
            self._redis.hset(callback, mapping=self._prepare_data())

        use_count = self._redis.hget(callback, 'use_count')
        self._increase_use_count(callback, use_count)
        self._redis.expire(callback, self._config.cache_time_limit)

    def remove_callback(self, callback: str):
        if not self._check_callback_existing(callback):
            return
        callback_fields = self._get_callback_fields_on_callback(callback)
        use_count = callback_fields[b'use_count']
        self._reduce_use_count(callback, int(use_count))
        if use_count == 1:
            self._pointers.append(callback_fields[b'abbreviation'].decode('utf-8'))
            self._redis.delete(callback)

    def _reduce_use_count(self, callback: str, use_count: int):
        self._redis.hset(callback, 'use_count', use_count - 1)

    def _increase_use_count(self, callback: str, use_count: int):
        self._redis.hset(callback, 'use_count', use_count + 1)

    def _prepare_data(self) -> dict:
        now = datetime.now()

        while self._check_abbreviation_existing(self._counter.count):
            self._counter.increment()
        return {

            'abbreviation': self._counter.count,
            'created_at': now,
            'updated_ad': now,
            'use_count': 0
        }

    def get_callback(self, abbreviation: str) -> str:
        abbreviation = abbreviation.encode()
        for callback in self._redis.keys():
            if abbreviation == self.get_abbreviation(callback):
                return callback.decode('utf-8')

    def get_abbreviation(self, callback: str) -> str:
        return self._redis.hget(callback, 'abbreviation')

    def _get_callback_fields_on_callback(self, callback: str):
        return self._redis.hgetall(callback)

    def _check_callback_existing(self, callback: str) -> bool:
        return self._redis.exists(callback)

    def _check_abbreviation_existing(self, abbreviation: str) -> bool:
        return bool(self.get_callback(abbreviation))

    def on_callbacks_exceeding_time_limit(self, cache_time_limit):
        self.nullify()
        return cache_time_limit

    def clear(self):
        self._pointers = list()
        self.nullify()
        self._redis.flushall()

    def nullify(self):
        self._counter.nullify()

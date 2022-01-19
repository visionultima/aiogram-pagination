from .base_storage import BaseCallbackStorage
from .builtin_storage import BuiltinCallbackStorage

try:
    from .redis_storage import RedisCallbackStorage
except ImportError:
    RedisCallbackStorage = None

try:
    from .sqlite_storage import SQLiteCallbackStorage
except ImportError:
    SQLiteCallbackStorage = None


class Storages:

    __storages = {
        'built-in': BuiltinCallbackStorage,
        'redis': RedisCallbackStorage,
        'sqlite': SQLiteCallbackStorage
    }

    def add_storage(self, name: str, value: BaseCallbackStorage):
        self.__storages[name] = value

    def get_storage(self, name: str) -> BaseCallbackStorage:
        return self.__storages[name]()

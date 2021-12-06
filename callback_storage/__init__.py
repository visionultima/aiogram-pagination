from contextlib import suppress
from enum import Enum

from .builtin_storage import BuiltinCallbackStorage
from .sqlite_storage import SQLiteCallbackStorage

with suppress(ImportError):
    from .redis_storage import RedisCallbackStorage


class Storages(Enum):
    builtin = BuiltinCallbackStorage
    sqlite = SQLiteCallbackStorage
    with suppress(NameError):
        redis = RedisCallbackStorage

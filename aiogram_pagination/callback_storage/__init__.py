from contextlib import suppress
from enum import Enum

from .builtin_storage import BuiltinCallbackStorage

with suppress(ImportError):
    from .sqlite_storage import SQLiteCallbackStorage
with suppress(ImportError):
    from .redis_storage import RedisCallbackStorage


class Storages(Enum):
    builtin = BuiltinCallbackStorage
    with suppress(NameError):
        sqlite = SQLiteCallbackStorage
    with suppress(NameError):
        redis = RedisCallbackStorage

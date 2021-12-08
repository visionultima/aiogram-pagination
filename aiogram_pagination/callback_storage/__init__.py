from contextlib import suppress
from enum import Enum

from .builtin_storage import BuiltinCallbackStorage

with suppress(ImportError):
    from .sqlite_storage import SQLiteCallbackStorage
with suppress(ImportError):
    from .redis_storage import RedisCallbackStorage


class StorageEnum(Enum):
    builtin = BuiltinCallbackStorage
    with suppress(NameError):
        sqlite = SQLiteCallbackStorage
    with suppress(NameError):
        redis = RedisCallbackStorage


class Storages:

    def __init__(self):
        self.storages = StorageEnum

    def get_storage(self, config):
        return self.storages[config['storage']].value()

    def add_storage(self, name, value):
        self.storages = Enum(
            'Storages',
            [(storage.name, storage.value) for storage in self.storages] + [(name, value)]
        )

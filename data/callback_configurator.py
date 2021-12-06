import os
import pathlib
from enum import Enum
from pathlib import Path

from bestconfig import Config

from callback_storage import Storages


class CallbackConfigurator:

    def __init__(self):
        self.BASE_DIR = os.path.abspath(os.curdir)
        self.config = Config(*self.config_files).callback_stack
        self.storages = Storages

    @property
    def config_files(self):
        return [
            os.path.join(folder, file) for folder in (
                f'{self.BASE_DIR}/data/',
                f'{pathlib.Path(__file__).parent.absolute()}/',
                f'{self.BASE_DIR}/',
            )
            for file in os.listdir(folder) if Path(file).suffix in (
                '.json', '.env', '.ini', '.cfg'
            )
        ]

    def get_storage(self, config):
        return self.storages[config['storage']].value()

    def add_storage(self, name, value):
        self.storages = Enum(
            'CallbackStorages',
            [(storage.name, storage.value) for storage in self.storages] + [(name, value)]
        )

from pathlib import Path
import pathlib
import os

from bestconfig.config_provider import ConfigProvider
import bestconfig


class Config:

    def __init__(self):
        self.BASE_DIR = os.curdir
        self.config = bestconfig.Config(*self.config_files)
        self.config = ConfigProvider(self.config.callback_stack | self.config.callback_storage)

    @property
    def config_files(self):
        return [
            os.path.join(folder, file) for folder in (
                f'{self.BASE_DIR}/data/',
                f'{pathlib.Path(__file__).parent.absolute()}/',
                f'{self.BASE_DIR}/',
            ) if os.path.exists(folder)

            for file in os.listdir(folder) if Path(file).suffix in (
                '.json', '.ini', '.cfg', 'yml'
            )
        ]


config = Config().config

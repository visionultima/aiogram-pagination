import os
import pathlib
from pathlib import Path

from bestconfig import Config


class CallbackConfigurator:

    def __init__(self):
        self.BASE_DIR = os.path.abspath(os.curdir)
        self.config = Config(*self.config_files).callback_stack

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

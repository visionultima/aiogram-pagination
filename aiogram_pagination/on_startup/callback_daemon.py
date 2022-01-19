import time

from aiogram_pagination.data.config import config
from aiogram_pagination.callback_chain.compression.callback_storage import Storages


class CallbackDaemon:

    def __init__(self):
        self.config = config
        self.cache_time_limit = self.config.cache_time_limit
        self.callback_storage = Storages().get_storage(self.config.storage)

    def run_callback_daemon(self):
        while True:
            self.callback_storage.on_callbacks_exceeding_time_limit(self.cache_time_limit)
            time.sleep(self.cache_time_limit)

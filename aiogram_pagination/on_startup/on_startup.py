from threading import Thread

from aiogram_pagination.on_startup.callback_daemon import CallbackDaemon
from aiogram_pagination.data.config import config


def on_startup():
    if config.get('cache_time_limit'):
        callback_daemon = CallbackDaemon()
        thread = Thread(target=callback_daemon.run_callback_daemon)
        thread.start()

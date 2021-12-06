from threading import Thread

from .callback_daemon import CallbackDaemon


def on_startup():
    callback_daemon = CallbackDaemon()
    thread = Thread(target=callback_daemon.run_callback_daemon)
    thread.start()

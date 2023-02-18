import time
from threading import Thread, Event, Timer

from configurations import logger
from handlers.handler_exception import DisconnectionEvent
from mappings import TYPES


class Events:
    change_input = Event()
    connect = Event()
    clean = Event()
    disconnect = Event()
    set_device = Event()
    scan_sensor = Event()
    interval = Event()

    class Finish:
        connect = Event()
        clean = Event()


class StoppableThread(Thread):
    def __init__(self, target=None, name=None, args=(), kwargs=None, daemon=None, interval=None):
        super(StoppableThread, self).__init__(target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.events = Events()
        self.handler_name = ''
        self._interval = interval

    def set_handler(self, handler_name):
        self.events.change_input.set()
        self.events.Finish.connect.clear()
        self.handler_name = handler_name if handler_name in TYPES else ''
        return TYPES[self.handler_name].auto_connect

    def connect_handler(self, **kwargs):
        if self.handler_name:
            self.events.disconnect.clear()
            TYPES[self.handler_name].is_connected = TYPES[self.handler_name].connect(**kwargs)
            if TYPES[self.handler_name].is_connected:
                self.events.Finish.connect.set()
                self.events.interval.set()
                logger.debug(f'connected to handler {self.handler_name}')
            else:
                logger.error(f'Failed to connect to handler {self.handler_name}')
                self.events.disconnect.set()

    def cleanup(self):
        if not self.events.clean.is_set():
            self.events.clean.set()
        self._target(*self._args, **self._kwargs)
        logger.debug('clean current data')
        self.events.Finish.clean.wait()
        self.events.clean.clear()
        self.events.Finish.clean.clear()

    def run(self) -> None:
        while True:
            time.sleep(0.001)
            if self.events.change_input.is_set():
                self.events.clean.set()
                self.events.disconnect.clear()
                self.events.change_input.clear()
            if self.events.clean.is_set():
                self.cleanup()
            elif self.events.Finish.connect.is_set():
                try:
                    self._target(*self._args, **self._kwargs)
                    if self.events.interval.is_set():
                        self.events.interval.clear()
                        TYPES[self.handler_name].interval_action()
                        Timer(self._interval, lambda: self.events.interval.set()).start()
                except DisconnectionEvent as disconnect:
                    logger.error(disconnect)
                    self.events.clean.set()
                    self.events.disconnect.set()
                    self.events.Finish.connect.clear()

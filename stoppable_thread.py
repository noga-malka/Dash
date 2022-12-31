import time
from threading import Thread, Event

from configurations import logger
from consts import IS_DEBUG
from handlers.bluethooth_reader import BluetoothHandler
from handlers.file_handler import FileHandler
from handlers.handler_exception import DisconnectionEvent
from handlers.random_handler import RandomHandler
from handlers.serial_reader import SerialHandler

types = {'serial': SerialHandler(), 'bluetooth': BluetoothHandler(), 'upload': FileHandler()}
if IS_DEBUG:
    types['random'] = RandomHandler()


class Events:
    change_input = Event()
    connect = Event()
    clean = Event()
    disconnect = Event()
    set_device = Event()

    class Finish:
        connect = Event()
        clean = Event()


class StoppableThread(Thread):
    def __init__(self, target=None, name=None, args=(), kwargs=None, daemon=None):
        super(StoppableThread, self).__init__(target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.events = Events()
        self.handler_name = ''

    def set_handler(self, handler_name):
        self.events.change_input.set()
        self.events.Finish.connect.clear()
        self.handler_name = handler_name if handler_name in types else ''
        return types[self.handler_name].auto_connect

    def connect_handler(self, **kwargs):
        if self.handler_name:
            self.events.disconnect.clear()
            types[self.handler_name].is_connected = types[self.handler_name].connect(**kwargs)
            if types[self.handler_name].is_connected:
                self.events.Finish.connect.set()
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
                except DisconnectionEvent as disconnect:
                    logger.error(disconnect)
                    self.events.clean.set()
                    self.events.disconnect.set()
                    self.events.Finish.connect.clear()

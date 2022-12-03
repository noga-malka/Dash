import time
from threading import Thread, Event

from handlers.bluethooth_reader import BluetoothHandler
from handlers.file_handler import FileHandler
from handlers.random_handler import RandomHandler
from handlers.serial_reader import SerialHandler

types = {'serial': SerialHandler(), 'bluetooth': BluetoothHandler(), 'random': RandomHandler(), 'upload': FileHandler()}


class Events:
    change_input = Event()
    connect = Event()
    clean = Event()

    class Finish:
        connect = Event()
        clean = Event()


class StoppableThread(Thread):
    def __init__(self, target=None, name=None, args=(), kwargs=None, daemon=None):
        super(StoppableThread, self).__init__(target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.events = Events()
        self.handler_name = ''

    def set_handler(self, handler_name):
        self.handler_name = handler_name if handler_name in types else ''
        self.events.change_input.set()

    def connect_handler(self, **kwargs):
        if self.handler_name:
            is_connected = types[self.handler_name].connect(**kwargs)
            if is_connected:
                self.events.Finish.connect.set()

    def cleanup(self):
        if not self.events.clean.is_set():
            self.events.clean.set()
        self._target(*self._args, **self._kwargs)
        self.events.Finish.clean.wait()
        self.events.clean.clear()
        self.events.Finish.clean.clear()

    def run(self) -> None:
        while True:
            time.sleep(0.001)
            if self.events.change_input.is_set():
                self.cleanup()
                self.events.change_input.clear()
                self.events.Finish.connect.wait()
            if self.events.clean.is_set():
                self.cleanup()
            elif self.events.Finish.connect.is_set():
                self._target(*self._args, **self._kwargs)

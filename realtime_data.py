from threading import Event

import pandas

from handlers.consts import HardwarePackets
from stoppable_thread import StoppableThread, types


class RealtimeData:
    def __init__(self):
        self.thread = StoppableThread(target=self.add_data, daemon=True)
        self.thread.start()
        self.graph = pandas.DataFrame()
        self.command_outputs = {}
        self.mapping = {
            HardwarePackets.SETUP: self.setup,
            HardwarePackets.ONE_WIRE: self.save_output,
            HardwarePackets.DATA: self.add_row,
        }

    def in_types(self):
        return self.thread.handler_name in types

    def read_data(self):
        return self.graph.iloc[-1]

    def add_data(self):
        if self.thread.events.clean.is_set():
            self.graph = pandas.DataFrame()
            self.thread.events.Finish.clean.set()
        else:
            try:
                command, content = types[self.thread.handler_name].extract_data()
            except TypeError:
                return
            self.mapping[command](command, content)

    def save_output(self, command: str, content):
        self.command_outputs[command] = content
        self.thread.events.scan_sensor.set()

    def setup(self, command: str, content):
        self.command_outputs[command] = content
        self.thread.events.set_device.set()

    def add_row(self, command: str, content):
        self.graph = pandas.concat([self.graph, content])

    def clean(self):
        self.thread.events.clean.set()

    def send_command(self, command: str, content: str = '0', event: Event = None, timeout=5):
        if not event:
            types[self.thread.handler_name].send_command(command, content)
            return False
        event.clear()
        types[self.thread.handler_name].send_command(command, content)
        event.wait(timeout=timeout)
        return event.is_set()


realtime = RealtimeData()

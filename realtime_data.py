from threading import Event
from typing import Callable

import pandas

from configurations import Settings, logger
from handlers.consts import HardwarePackets
from stoppable_thread import StoppableThread, types


class RealtimeData:
    def __init__(self):
        self.thread = StoppableThread(target=self.add_data, daemon=True)
        self.thread.start()
        self.graph = pandas.DataFrame()
        self.command_outputs = {}
        self.mapping: dict[str, Callable] = {
            HardwarePackets.SETUP: self.setup,
            HardwarePackets.ONE_WIRE: self.save_output,
            HardwarePackets.DATA: self.add_row,
            HardwarePackets.FILE: self.add_dataframe,
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
            data = []
            try:
                data = types[self.thread.handler_name].extract_data()
                for (command, content) in data:
                    self.mapping[command](command, content)
            except (KeyError, IndexError, ValueError, UnicodeDecodeError):
                logger.warning(f'Failed to parse row: {data}')

    def save_output(self, command: str, content: str):
        self.command_outputs[command] = int(content[0])
        self.thread.events.scan_sensor.set()

    def setup(self, command: str, content: str):
        self.command_outputs[command] = content
        self.thread.events.set_device.set()

    def add_row(self, command: str, content: str):
        sample = {content[index]: float(content[index + 1]) for index in range(0, len(content), 2)}
        sample = {key: value for key, value in sample.items() if key in Settings.SENSORS}
        content = pandas.DataFrame(sample, index=[pandas.Timestamp.now()])
        self.add_dataframe(command, content)

    def add_dataframe(self, command: str, dataframe: pandas.DataFrame):
        self.graph = pandas.concat([self.graph, dataframe])

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

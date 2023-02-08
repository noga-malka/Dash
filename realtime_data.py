from threading import Event
from typing import Callable

import pandas

from configurations import Settings, logger
from dataframe import Dataframe
from handlers.consts import HardwarePackets
from stoppable_thread import StoppableThread, types


class RealtimeData:
    def __init__(self):
        self.thread = StoppableThread(target=self.add_data, daemon=True)
        self.thread.start()
        self.data = Dataframe()
        self.current = {}
        self.command_outputs = {}
        self.mapping: dict[str, Callable] = {
            HardwarePackets.SETUP: self.setup,
            HardwarePackets.ONE_WIRE: self.save_output,
            HardwarePackets.DATA: self.add_row,
            HardwarePackets.FILE: self.add_dataframe,
            HardwarePackets.DPC: self.parse_dpc_controller,
        }

    def in_types(self):
        return self.thread.handler_name in types

    def read_data(self):
        return self.data.read_row()

    def add_data(self):
        if self.thread.events.clean.is_set():
            self.data.reset(self.thread.events.Finish.clean)
        else:
            data = []
            try:
                self.current = {}
                data = types[self.thread.handler_name].extract_data()
                for (command, content) in data:
                    data_type, args = self.mapping[command](command, content)
                    self.current.setdefault(data_type, [])
                    self.current[data_type].append(args)
                if self.current:
                    self.data.save(self.current)
            except (KeyError, IndexError, ValueError, UnicodeDecodeError):
                logger.warning(f'Failed to parse row: {data}')

    def parse_dpc_controller(self, command: str, content: str):
        try:
            parsed_content = float(content[0].strip('>'))
        except (ValueError, IndexError):
            return 'ignore',
        return 'row', {'dpc': parsed_content}

    def save_output(self, command: str, content: str):
        print(command, content)
        return 'single', (command, int(content[0]), self.thread.events.scan_sensor)

    def setup(self, command: str, content: str):
        return 'single', (command, content, self.thread.events.set_device)

    def add_row(self, command: str, content: str):
        sample = {content[index]: float(content[index + 1]) for index in range(0, len(content), 2)}
        return 'row', {key: value for key, value in sample.items() if key in Settings.SENSORS}

    def add_dataframe(self, command: str, dataframe: pandas.DataFrame):
        return 'frame', dataframe

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

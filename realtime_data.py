from threading import Event
from typing import Callable

import pandas

from configurations import Settings, logger
from consts import DatabaseTypes
from database_manager import DatabaseManager
from handlers.consts import HardwarePackets
from handlers.handler_exception import DisconnectionEvent
from mappings.handlers import TYPES
from stoppable_thread import StoppableThread


class RealtimeData:
    def __init__(self):
        self.thread = StoppableThread(target=self.add_data, daemon=True, interval=0.8)
        self.thread.start()
        self.database = DatabaseManager()
        self._current = {}

        self._mapping: dict[str, Callable] = {
            HardwarePackets.SETUP: self.setup,
            HardwarePackets.ONE_WIRE: self.save_output,
            HardwarePackets.DATA: self.add_row,
            HardwarePackets.FILE: self.add_dataframe,
        }

    def in_types(self):
        return self.thread.handler_name in TYPES

    def add_data(self):
        if self.thread.events.clean.is_set():
            self.database.reset(self.thread.events.Finish.clean)
        else:
            data = []
            try:
                self._current = {}
                data = TYPES[self.thread.handler_name].extract_data()
                for (command, content) in data:
                    data_type, args = self._mapping[command](command=command, content=content)
                    self._current.setdefault(data_type, [])
                    self._current[data_type].append(args)
                self.database.save(self._current)
            except (KeyError, IndexError, ValueError, UnicodeDecodeError):
                logger.warning(f'Failed to parse row: {data}')

    def save_output(self, command: str, content: str, **kwargs):
        return DatabaseTypes.SINGLE_VALUE, (command, int(content[0]), self.thread.events.scan_sensor)

    def setup(self, command: str, content: str, **kwargs):
        return DatabaseTypes.SINGLE_VALUE, (command, content, self.thread.events.set_device)

    @staticmethod
    def add_row(content: str, **kwargs):
        sample = {}
        for index in range(0, len(content), 2):
            try:
                data = float(content[index + 1])
            except ValueError:
                data = content[index + 1]
            sample[content[index]] = data
        return DatabaseTypes.ROW, {key: value for key, value in sample.items() if key in Settings.SENSORS}

    @staticmethod
    def add_dataframe(content: pandas.DataFrame, **kwargs):
        return DatabaseTypes.DATAFRAME, content

    def send_command(self, command: str, content: str = '0', event: Event = None, timeout=5, input_type=None):
        try:
            if not event:
                TYPES[self.thread.handler_name].send_command(command, content, input_type)
                return False
            event.clear()
            TYPES[self.thread.handler_name].send_command(command, content, input_type)
            event.wait(timeout=timeout)
            return event.is_set()
        except DisconnectionEvent as disconnect:
            realtime.thread.disconnect(disconnect)
            return False


realtime = RealtimeData()

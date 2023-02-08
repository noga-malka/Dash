from threading import Event
from typing import Callable

import pandas

from configurations import Settings, logger, InputNames
from consts import DatabaseTypes
from database_manager import DatabaseManager
from handlers.consts import HardwarePackets
from stoppable_thread import StoppableThread, types


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
            HardwarePackets.DPC: self.parse_dpc_controller,
        }

    def in_types(self):
        return self.thread.handler_name in types

    def add_data(self):
        if self.thread.events.clean.is_set():
            self.database.reset(self.thread.events.Finish.clean)
        else:
            data = []
            try:
                self._current = {}
                data = types[self.thread.handler_name].extract_data()
                for (command, content) in data:
                    data_type, args = self._mapping[command](command=command, content=content)
                    self._current.setdefault(data_type, [])
                    self._current[data_type].append(args)
                self.database.save(self._current)
            except (KeyError, IndexError, ValueError, UnicodeDecodeError):
                logger.warning(f'Failed to parse row: {data}')

    @staticmethod
    def parse_dpc_controller(content: str, **kwargs):
        try:
            row = {InputNames.DPC: float(content[0])}
        except (ValueError, IndexError):
            row = {}
        return DatabaseTypes.ROW, row

    def save_output(self, command: str, content: str, **kwargs):
        return DatabaseTypes.SINGLE_VALUE, (command, int(content[0]), self.thread.events.scan_sensor)

    def setup(self, command: str, content: str, **kwargs):
        return DatabaseTypes.SINGLE_VALUE, (command, content, self.thread.events.set_device)

    @staticmethod
    def add_row(content: str, **kwargs):
        sample = {content[index]: float(content[index + 1]) for index in range(0, len(content), 2)}
        return DatabaseTypes.ROW, {key: value for key, value in sample.items() if key in Settings.SENSORS}

    @staticmethod
    def add_dataframe(content: pandas.DataFrame, **kwargs):
        return DatabaseTypes.DATAFRAME, content

    def send_command(self, command: str, content: str = '0', event: Event = None, timeout=5):
        if not event:
            types[self.thread.handler_name].send_command(command, content)
            return False
        event.clear()
        types[self.thread.handler_name].send_command(command, content)
        event.wait(timeout=timeout)
        return event.is_set()


realtime = RealtimeData()

from threading import Event
from typing import Callable

import pandas

from configurations import logger, InputNames
from consts import DatabaseTypes
from database_manager import DatabaseManager
from handlers.consts import HardwarePackets, DataColumns
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
            HardwarePackets.DATA: self.add_live_row,
            HardwarePackets.PLAYBACK: self.add_playback_row,
            HardwarePackets.PLAYBACK_END: self.end_playback,
            HardwarePackets.FILE: self.add_dataframe,
            HardwarePackets.DEVICE_ID: self.save_single_output,
            HardwarePackets.SOFTWARE_VERSION: self.save_single_output,
            HardwarePackets.CLOCK: self.save_single_output,
            HardwarePackets.TOTAL_TIME: self.save_single_output,
            HardwarePackets.RUN_TIME: self.save_single_output,
            HardwarePackets.FILES_LIST: self.save_multiple_outputs,
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
            except (KeyError, IndexError, ValueError, UnicodeDecodeError, TypeError):
                logger.warning(f'Failed to parse row: {data}')

    @staticmethod
    def save_multiple_outputs(command: str, content: str, **kwargs):
        return DatabaseTypes.SINGLE_VALUE, (command, content, None)

    @staticmethod
    def save_single_output(command: str, content: str, **kwargs):
        return DatabaseTypes.SINGLE_VALUE, (command, content[0], None)

    @staticmethod
    def add_row(content: str, **kwargs):
        sample = {}
        for index in range(0, len(content), 2):
            try:
                data = float(content[index + 1])
            except ValueError:
                data = content[index + 1]
            sample[content[index]] = data
        return sample

    def end_playback(self, content: str, **kwargs):
        self.thread.events.live_mode.set()
        return DatabaseTypes.IGNORE, content

    def add_live_row(self, content: str, **kwargs):
        return DatabaseTypes.ROW, self.add_row(content)

    @staticmethod
    def add_playback_row(content: str, **kwargs):
        if len(content[0].split(',')) == DataColumns.COUNT:
            return DatabaseTypes.PLAYBACK, content[0]

    @staticmethod
    def add_dataframe(content: pandas.DataFrame, **kwargs):
        return DatabaseTypes.DATAFRAME, content

    def send_command(self, command: str, content: str = '0', event: Event = None, timeout=5, content_length: int = 2):
        try:
            if not event:
                TYPES[self.thread.handler_name].send_command(command, content, content_length)
                return False
            event.clear()
            TYPES[self.thread.handler_name].send_command(command, content, content_length)
            event.wait(timeout=timeout)
            return event.is_set()
        except DisconnectionEvent as disconnect:
            realtime.thread.disconnect(disconnect)
            return False

    def is_recording(self) -> bool:
        if self.database.is_not_empty():
            return self.database.read().get(InputNames.RECORD_STATUS) == 'Recording'
        return False


realtime = RealtimeData()

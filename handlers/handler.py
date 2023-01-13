from typing import Union

import pandas

from configurations import Settings, logger
from consts import Commands, HardwarePackets


class Handler:
    def __init__(self, auto_connect=True):
        self.client = None
        self.is_connected = False
        self.current = ''
        self.auto_connect = auto_connect
        self.mapping = {
            HardwarePackets.SETUP: self.setup,
            HardwarePackets.ONE_WIRE: self.one_wire,
            HardwarePackets.DATA: self.parse_data,
        }

    def connect(self, **kwargs):
        raise NotImplementedError()

    def disconnect(self):
        if self.client:
            self.client.close()
        self.client = None

    def send_command(self, command, content):
        raise NotImplementedError()

    def read_line(self):
        raise NotImplementedError()

    def extract_data(self):
        if self.is_connected:
            line = self.read_line()
            try:
                command, *content = line.split('\t')
                return self.mapping[command](command, content)
            except (KeyError, IndexError, ValueError, UnicodeDecodeError):
                logger.warning(f'Failed to parse row: {line}')

    @staticmethod
    def setup(command: str, content: list):
        return command, content

    @staticmethod
    def one_wire(command: str, content: list):
        return command, int(content[0])

    @staticmethod
    def parse_data(command: str, content: list):
        sample = {content[index]: float(content[index + 1]) for index in range(0, len(content), 2)}
        sample = {key: value for key, value in sample.items() if key in Settings.SENSORS}
        return command, pandas.DataFrame(sample, index=[pandas.Timestamp.now()])

    @staticmethod
    def format(value: Union[str, int], byte_number: int = 1):
        formatter = f'{{:0>{byte_number * 2}}}'
        return formatter.format(value)

    def build_command(self, command, content):
        content = self.format(hex(int(content)).replace('0x', ''), byte_number=2)
        command = self.format(hex(int(command)).replace('0x', ''))
        length = self.format(int(len(content) / 2))
        return bytes.fromhex(Commands.HEADER + command + length + content)

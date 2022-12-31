from typing import Union

import pandas

from configurations import Settings, logger
from consts import Commands


class Handler:
    def __init__(self, auto_connect=True):
        self.client = None
        self.is_connected = False
        self.current = ''
        self.auto_connect = auto_connect

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
        if not self.is_connected:
            return pandas.DataFrame(), True
        line = self.read_line()
        try:
            data = line.split('\t')
            if data[0] in ['setup']:
                return data, False
            sample = {data[index]: float(data[index + 1]) for index in range(0, len(data), 2)}
            sample = {key: value for key, value in sample.items() if key in Settings.SENSORS}
            return pandas.DataFrame(sample, index=[pandas.Timestamp.now()]), True
        except (KeyError, IndexError, ValueError):
            logger.warning(f'Failed to parse row: {line}')
            return pandas.DataFrame(), True

    @staticmethod
    def format(value: Union[str, int], byte_number: int = 1):
        formatter = f'{{:0>{byte_number * 2}}}'
        return formatter.format(value)

    def build_command(self, command, content):
        content = self.format(hex(int(content)).replace('0x', ''), byte_number=2)
        command = self.format(command)
        length = self.format(int(len(content) / 2))
        return bytes.fromhex(Commands.HEADER + command + length + content)

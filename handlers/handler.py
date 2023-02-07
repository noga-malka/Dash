from typing import Union

from configurations import logger
from handlers.consts import Commands


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
        if self.is_connected:
            output = self.read_line()
            try:
                parsed_data = []
                for line in output:
                    command, *content = line.split('\t')
                    parsed_data.append((command, content))
                return parsed_data
            except (KeyError, IndexError, ValueError, UnicodeDecodeError):
                logger.warning(f'Failed to parse row: {output}')

    @staticmethod
    def format(value: Union[str, int], byte_number: int = 1):
        formatter = f'{{:0>{byte_number * 2}}}'
        return formatter.format(value)

    def build_command(self, command, content):
        content = self.format(hex(int(content)).replace('0x', ''), byte_number=2)
        command = self.format(hex(int(command)).replace('0x', ''))
        length = self.format(int(len(content) / 2))
        return bytes.fromhex(Commands.HEADER + command + length + content)

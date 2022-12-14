from typing import Union

import pandas

from configurations import Settings, logger


class Handler:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.retry_delay = 60

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
        line = self.read_line()
        try:
            data = line.split('\t')
            sample = {data[index]: float(data[index + 1]) for index in range(0, len(data), 2)}
            invalid_keys = [key for key in sample if key not in Settings.SENSORS]
            if len(invalid_keys):
                logger.warning(f'Unknown sensors: {invalid_keys}')
                return pandas.DataFrame()
            sample = pandas.DataFrame(sample, index=[pandas.Timestamp.now()])
            return sample
        except (KeyError, IndexError, ValueError):
            logger.warning(f'Failed to parse row: {line}')
            return pandas.DataFrame()

    @staticmethod
    def format(value: Union[str, int], byte_number: int = 1):
        formatter = f'{{:0>{byte_number * 2}}}'
        return formatter.format(value)

import time

import pandas

from realtime_data import realtime


class Handler:
    def __init__(self):
        self.client = None
        self.is_connected = self.connect()
        self.retry_delay = 60

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        if self.client:
            self.client.close()
        self.client = None

    def read_line(self):
        raise NotImplementedError()

    def extract_data(self):
        if not self.is_connected:
            print(f'failed to connect to live stream. retry in {self.retry_delay} seconds')
            time.sleep(self.retry_delay)
            self.is_connected = self.connect()
        else:
            try:
                data = self.read_line().strip().split('\t')
                sample = {data[index]: float(data[index + 1]) for index in range(0, len(data), 2)}
                sample = pandas.DataFrame(sample, index=[pandas.Timestamp.now()])
                realtime.add(sample)
            except (KeyError, IndexError, ValueError) as error:
                pass

import base64
from io import StringIO

import pandas

from handlers.consts import HardwarePackets
from handlers.handler import Handler
from utilities import packet_sender


class FileHandler(Handler):
    COLUMNS = ['Time', 'Temp', 'Vbat', 'Fan', 'Tach', 'Tach2']

    def __init__(self):
        super(FileHandler, self).__init__(False)
        self.is_loaded = False
        self.content = None

    @packet_sender
    def send_command(self, packet):
        pass

    def connect(self, content=None, file_name=None):
        if content:
            self.is_loaded = False
            self.current = file_name
            data = content.encode("utf8").split(b";base64,")[1]
            data = StringIO(base64.decodebytes(data).decode('utf8'))
            self.content = pandas.read_csv(data, usecols=list(range(1, 10, 2)), names=self.COLUMNS)
            return True
        return False

    def read_lines(self) -> list[str]:
        pass

    def extract_data(self):
        content = self.content if not self.is_loaded else pandas.DataFrame
        if not self.is_loaded:
            self.is_loaded = True
        return [(HardwarePackets.FILE, content)]

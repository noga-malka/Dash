import base64
from io import StringIO

import pandas

from handlers.consts import HardwarePackets
from handlers.handler import Handler


class FileHandler(Handler):
    def __init__(self):
        super(FileHandler, self).__init__(False)
        self.is_loaded = False
        self.content = None

    def send_command(self, command, content):
        pass

    def connect(self, content=None, file_name=None):
        if content:
            self.is_loaded = False
            self.current = file_name
            data = content.encode("utf8").split(b";base64,")[1]
            data = StringIO(base64.decodebytes(data).decode('utf8'))
            self.content = pandas.read_csv(data, index_col=0)
            return True
        return False

    def read_lines(self) -> list[str]:
        pass

    def extract_data(self):
        content = self.content if not self.is_loaded else pandas.DataFrame
        if not self.is_loaded:
            self.is_loaded = True
        return [(HardwarePackets.FILE, content)]

import base64
from io import StringIO

import pandas

from handlers.handler import Handler


class FileHandler(Handler):
    def __init__(self):
        super(FileHandler, self).__init__()
        self.is_loaded = False
        self.content = None

    def send_command(self, command, content):
        pass

    def connect(self, content=None):
        if content:
            data = content.encode("utf8").split(b";base64,")[1]
            data = StringIO(base64.decodebytes(data).decode('utf8'))
            self.content = pandas.read_csv(data, index_col=0)
            return True
        return False

    def read_line(self) -> str:
        pass

    def extract_data(self):
        if not self.is_loaded:
            return self.content
        else:
            return pandas.DataFrame()

import socket

from consts import Bluetooth
from handlers.handler import Handler


class BluetoothHandler(Handler):
    def __init__(self, address=Bluetooth.DEFAULT_ADDRESS):
        self.buffer = ''
        self.address = address
        super(BluetoothHandler, self).__init__()

    def connect(self, **kwargs):
        self.disconnect()
        try:
            self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.client.connect((self.address, 1))
        except OSError:
            self.client = None
            return False
        return True

    def read_line(self) -> str:
        self.buffer = ''
        while '\n' not in self.buffer:
            self.buffer += self.client.recv(1024).decode()
        return self.buffer

    def send_command(self, command, content):
        pass

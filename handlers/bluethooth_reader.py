import bluetooth

from consts import Bluetooth
from handlers.handler import Handler


class BluetoothHandler(Handler):
    def __init__(self, address=Bluetooth.DEFAULT_ADDRESS):
        self.buffer = ''
        self.address = address
        super(BluetoothHandler, self).__init__()

    def connect(self):
        self.disconnect()
        try:
            self.client = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
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

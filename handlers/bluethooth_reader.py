import socket

import bluetooth

from handlers.handler import Handler
from handlers.handler_exception import DisconnectionEvent
from utilities import packet_sender


class BluetoothHandler(Handler):
    def __init__(self):
        self.buffer = b''
        self.devices = {}
        super(BluetoothHandler, self).__init__(False)

    @staticmethod
    def discover():
        return dict(bluetooth.discover_devices(lookup_names=True))

    def connect(self, address='', label=None, **kwargs):
        self.disconnect()
        try:
            self.buffer = b''
            self.current = label if label else address
            self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.client.connect((address, 1))
        except OSError:
            self.client = None
            return False
        return True

    def read_lines(self) -> list[str]:
        while b'\n' not in self.buffer:
            try:
                new_data = self.client.recv(4096)
                if new_data == b'':
                    raise ConnectionAbortedError
            except ConnectionAbortedError:
                raise DisconnectionEvent(self.__class__.__name__)
            self.buffer += new_data
        end_line = self.buffer.find(b'\n')
        output = self.buffer[:end_line]
        self.buffer = self.buffer[end_line + 1:]
        return [output.decode()]

    @packet_sender
    def send_command(self, packet):
        self.send(packet)

    def send(self, packet):
        self.client.send(packet)

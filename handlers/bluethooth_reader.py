import socket

import bluetooth

from configurations import logger
from handlers.handler import Handler
from handlers.handler_exception import DisconnectionEvent


class BluetoothHandler(Handler):
    def __init__(self):
        self.buffer = b''
        self.devices = {}
        super(BluetoothHandler, self).__init__(False)

    def discover(self):
        self.devices = {name: mac for (mac, name) in bluetooth.discover_devices(lookup_names=True)}

    def connect(self, address='', **kwargs):
        self.disconnect()
        try:
            self.buffer = b''
            self.current = address
            self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.client.connect((self.devices.get(address, ''), 1))
        except OSError:
            self.client = None
            return False
        return True

    def read_lines(self) -> list[str]:
        while b'\n' not in self.buffer:
            new_data = self.client.recv(4096)
            if new_data == b'':
                raise DisconnectionEvent(self.__class__.__name__)
            self.buffer += new_data
        end_line = self.buffer.find(b'\n')
        output = self.buffer[:end_line]
        self.buffer = self.buffer[end_line + 1:]
        return [output.decode()]

    def send_command(self, command, content):
        packet = self.build_command(command, content)
        if self.client:
            logger.info(f'send packet: {packet}')
            self.client.send(packet)
        else:
            logger.warning(f'no connection. could not send {packet}')

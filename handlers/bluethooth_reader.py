import socket

from configurations import logger
from handlers.handler import Handler


class BluetoothHandler(Handler):
    def __init__(self):
        self.buffer = ''
        self.devices = {}
        super(BluetoothHandler, self).__init__(False)

    def connect(self, address='', **kwargs):
        self.disconnect()
        try:
            self.current = address
            self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.client.connect((self.devices.get(address, ''), 1))
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
        packet = self.build_command(command, content)
        if self.client:
            logger.info(f'send packet: {packet}')
            self.client.send(packet)
        else:
            logger.warning(f'no connection. could not send {packet}')

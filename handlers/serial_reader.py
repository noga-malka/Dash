import serial
from serial.tools import list_ports

from configurations import logger
from consts import Uart
from handlers.handler import Handler
from handlers.handler_exception import DisconnectionEvent


class SerialHandler(Handler):
    def __init__(self):
        self.devices = []
        super(SerialHandler, self).__init__(False)

    def discover(self):
        self.devices = [com[0] for com in filter(lambda port: "USB" in port[2], list_ports.comports())]

    def connect(self, comport=None, **kwargs):
        self.disconnect()
        try:
            self.current = comport
            self.client = serial.Serial(comport, Uart.BAUDRATE, timeout=Uart.TIMEOUT)
        except serial.SerialException:
            self.client = None
            return False
        return True

    def read_line(self) -> str:
        try:
            return self.client.readline().decode().strip()
        except serial.SerialException:
            raise DisconnectionEvent(self.__class__.__name__)

    def send_command(self, command: str, content: str):
        packet = self.build_command(command, content)
        if self.client:
            logger.info(f'send packet: {packet}')
            self.client.write(packet)
        else:
            logger.warning(f'no connection. could not send {packet}')

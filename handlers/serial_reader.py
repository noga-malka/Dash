import serial
from serial.tools import list_ports

from handlers.consts import Uart
from handlers.handler import Handler
from handlers.handler_exception import DisconnectionEvent
from utilities import packet_sender


class SerialHandler(Handler):
    def __init__(self):
        super(SerialHandler, self).__init__(False)

    @staticmethod
    def discover():
        return {com[0]: com[0] for com in filter(lambda port: "USB" in port[2], list_ports.comports())}

    def connect(self, address=None, **kwargs):
        self.disconnect()
        try:
            self.current = address
            self.client = serial.Serial(address, Uart.BAUDRATE, timeout=Uart.TIMEOUT)
        except serial.SerialException:
            self.client = None
            return False
        return True

    def read_lines(self) -> list[str]:
        try:
            if self.client.inWaiting():
                return [self.client.readline().decode().strip()]
        except (serial.SerialException, AttributeError):
            raise DisconnectionEvent(self.__class__.__name__)
        return []

    @packet_sender
    def send_command(self, packet, input_type=None):
        self.send(packet)

    def send(self, packet):
        self.client.write(packet)

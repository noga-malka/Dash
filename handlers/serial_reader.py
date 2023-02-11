import serial

from handlers.consts import Uart
from handlers.handler import Handler
from handlers.handler_exception import DisconnectionEvent
from utilities import packet_sender


class SerialHandler(Handler):
    def __init__(self):
        super(SerialHandler, self).__init__(False)

    def connect(self, comport=None, **kwargs):
        self.disconnect()
        try:
            self.current = comport
            self.client = serial.Serial(comport, Uart.BAUDRATE, timeout=Uart.TIMEOUT)
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
        self.client.write(packet)

import serial
from serial.tools import list_ports

from configurations import logger
from consts import Uart
from handlers.handler import Handler
from handlers.handler_exception import DisconnectionEvent


class SerialHandler(Handler):
    def __init__(self):
        self.devices = {}
        super(SerialHandler, self).__init__()

    def discover(self):
        self.devices = {com[0]: com[0] for com in filter(lambda port: "USB" in port[2], list_ports.comports())}

    def connect(self, **kwargs):
        self.disconnect()
        usb_ports = list(filter(lambda port: "USB" in port[2], list(list_ports.comports())))
        if len(usb_ports) == 1:
            self.current = usb_ports[0][0]
            self.client = serial.Serial(usb_ports[0][0], Uart.BAUDRATE, timeout=Uart.TIMEOUT)
            return True
        return False

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

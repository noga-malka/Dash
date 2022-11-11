import serial
from serial.tools import list_ports

from consts import Uart
from handlers.handler import Handler


class SerialHandler(Handler):
    def __init__(self):
        super(SerialHandler, self).__init__()

    def connect(self):
        self.disconnect()
        usb_ports = list(filter(lambda port: "USB" in port[2], list(list_ports.comports())))
        if len(usb_ports) == 1:
            self.client = serial.Serial(usb_ports[0][0], Uart.BAUDRATE, timeout=Uart.TIMEOUT)
            return True
        return False

    def read_line(self) -> str:
        return self.client.readline().decode()
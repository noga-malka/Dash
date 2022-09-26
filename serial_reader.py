import serial
from serial.tools import list_ports

from consts import Uart


class SerialHandler:
    def __init__(self):
        self.serial = None
        self.connect()

    def connect(self):
        self.disconnect()
        usb_ports = list(filter(lambda port: "USB" in port[2], list(list_ports.comports())))
        if len(usb_ports) == 1:
            self.serial = serial.Serial(usb_ports[0][0], Uart.BAUDRATE, timeout=Uart.TIMEOUT)
            return True
        return False

    def disconnect(self):
        if self.serial:
            self.serial.close()
        self.serial = None

    def read_line(self) -> str:
        return self.serial.readline().decode()

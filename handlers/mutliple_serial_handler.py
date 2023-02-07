from serial.tools import list_ports

from configurations import logger
from handlers.consts import Commands, InputTypes
from handlers.handler import Handler
from handlers.serial_reader import SerialHandler


class MultipleSerialHandler(Handler):
    def __init__(self):
        self.handlers = {}
        self.devices = []
        super(MultipleSerialHandler, self).__init__(False)

    def discover(self):
        self.devices = [com[0] for com in filter(lambda port: "USB" in port[2], list_ports.comports())]

    def connect(self, connections: dict, **kwargs):
        for comport, action in connections.items():
            self.handlers[action] = SerialHandler()
            self.handlers[action].is_connected = self.handlers[action].connect(comport=comport)
        self.current = list(connections)
        return all(handler.is_connected for handler in self.handlers.values())

    def send_command(self, command, content):
        for handler_name, commands in Commands.CLASSIFIER.items():
            if command in commands:
                self.handlers[handler_name].send_command(command, content)
                return
        logger.warning(f'no handler with command {command}')

    def read_lines(self) -> list[str]:
        lines = []
        for input_type, connection in self.handlers.items():
            lines += [InputTypes.HEADERS.get(input_type, '') + line for line in connection.read_lines()]
        return lines

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

    def disconnect(self):
        for connection in self.handlers.values():
            connection.disconnect()
        self.handlers = {}

    def connect(self, connections: dict, **kwargs):
        self.disconnect()
        for comport, action in connections.items():
            self.handlers[action] = SerialHandler()
            self.handlers[action].is_connected = self.handlers[action].connect(comport=comport)
        self.current = list(connections)
        return all(handler.is_connected for handler in self.handlers.values())

    def send_command(self, command, content):
        input_type = Commands.CLASSIFIER.get(command)
        try:
            packet = InputTypes.MAPPING[input_type]['packet_builder'].build_packet(command, content)
            self.handlers[input_type].send_packet(packet)
        except KeyError:
            logger.warning(f'no handler with command {command}')

    def interval_action(self):
        if InputTypes.CO2_CONTROLLER in self.handlers:
            self.send_command(Commands.CO2Controller.READ, '')

    def read_lines(self) -> list[str]:
        lines = []
        for input_type, connection in self.handlers.items():
            lines += [InputTypes.MAPPING[input_type]['header'] + line for line in connection.read_lines()]
        return lines

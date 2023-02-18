from handlers.consts import Commands, InputTypes
from handlers.handler import Handler
from handlers.serial_reader import SerialHandler
from mappings.controls import CONTROLS
from utilities import packet_sender


class MultipleSerialHandler(Handler):
    def __init__(self):
        self.handlers = {}
        super(MultipleSerialHandler, self).__init__(False)

    @staticmethod
    def discover():
        return SerialHandler.discover()

    def disconnect(self):
        for connection in self.handlers.values():
            connection.disconnect()
        self.handlers = {}

    def connect(self, connections: dict, **kwargs):
        self.disconnect()
        for comport, action in connections.items():
            self.handlers[action] = SerialHandler()
            self.handlers[action].is_connected = self.handlers[action].connect(address=comport)
        self.current = list(connections)
        return all(handler.is_connected for handler in self.handlers.values())

    @packet_sender
    def send_command(self, packet, input_type=None):
        self.handlers[input_type].client.write(packet)

    def interval_action(self):
        if InputTypes.CO2_CONTROLLER in self.handlers:
            self.send_command(Commands.CO2Controller.READ, '')

    def read_lines(self) -> list[str]:
        lines = []
        for input_type, connection in self.handlers.items():
            lines += [CONTROLS[input_type]['header'] + line for line in connection.read_lines()]
        return lines

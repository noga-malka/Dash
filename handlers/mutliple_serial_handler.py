import functools

from handlers.bluethooth_reader import BluetoothHandler
from handlers.consts import Commands, InputTypes
from handlers.handler import Handler
from handlers.serial_reader import SerialHandler
from mappings.controls import CONTROLS
from utilities import packet_sender


class MultipleInputsHandler(Handler):
    def __init__(self):
        self.handlers = {}
        self.types = [SerialHandler, BluetoothHandler]
        self.devices = {}
        super(MultipleInputsHandler, self).__init__(False)

    def discover(self):
        for handler_class in self.types:
            self.devices[handler_class.__name__] = handler_class.discover()
        return functools.reduce(lambda a, b: a | b, self.devices.values())

    def disconnect(self):
        for connection in self.handlers.values():
            connection.disconnect()
        self.handlers = {}

    def connect(self, connections: dict, labels: dict, **kwargs):
        self.disconnect()
        connection_status = True
        for address, action in connections.items():
            for handler_class in self.types:
                if address in self.devices[handler_class.__name__]:
                    self.handlers[action] = handler_class()
                    is_connected = self.handlers[action].connect(address=address, label=labels[address])
                    connection_status &= is_connected
        self.current = [labels[address] for address in connections]
        return connection_status

    @packet_sender
    def send_command(self, packet, input_type=None):
        self.handlers[input_type].send(packet)

    def interval_action(self):
        if InputTypes.CO2_CONTROLLER in self.handlers:
            self.send_command(Commands.CO2Controller.READ, '')

    def read_lines(self) -> list[str]:
        lines = []
        for input_type, connection in self.handlers.items():
            lines += [CONTROLS[input_type]['header'] + line for line in connection.read_lines()]
        return lines

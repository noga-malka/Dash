from utilities import packet_sender


class Handler:
    def __init__(self, auto_connect=True):
        self.client = None
        self.is_connected = False
        self.current = ''
        self.auto_connect = auto_connect

    def connect(self, **kwargs):
        raise NotImplementedError()

    def disconnect(self):
        if self.client:
            self.client.close()
        self.client = None

    def interval_action(self):
        pass

    @packet_sender
    def send_command(self, packet, input_type=None):
        raise NotImplementedError()

    def read_lines(self) -> list[str]:
        raise NotImplementedError()

    def extract_data(self):
        if self.is_connected:
            lines = self.read_lines()
            parsed_data = []
            for line in lines:
                command, *content = line.split('\t')
                parsed_data.append((command, content))
            return parsed_data

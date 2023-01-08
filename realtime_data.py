import pandas

from consts import HardwarePackets
from stoppable_thread import StoppableThread, types


class RealtimeData:
    def __init__(self):
        self.thread = StoppableThread(target=self.add_data, daemon=True)
        self.thread.start()
        self.graph = pandas.DataFrame()
        self.command_outputs = {}
        self.mapping = {
            HardwarePackets.SETUP: self.setup,
            HardwarePackets.ONE_WIRE: self.save_output,
            HardwarePackets.DATA: self.add_row,
        }

    def read_data(self):
        return self.graph.iloc[-1]

    def add_data(self):
        if self.thread.events.clean.is_set():
            self.graph = pandas.DataFrame()
            self.thread.events.Finish.clean.set()
        else:
            try:
                command, content = types[self.thread.handler_name].extract_data()
            except TypeError:
                return
            self.mapping[command](command, content)

    def save_output(self, command: str, content):
        self.command_outputs[command] = content

    def setup(self, command: str, content):
        self.thread.events.set_device.set()
        self.command_outputs[command] = content

    def add_row(self, command: str, content):
        self.graph = pandas.concat([self.graph, content])

    def clean(self):
        self.thread.events.clean.set()


realtime = RealtimeData()

import pandas

from consts import Sensors


class RealtimeData:
    def __init__(self):
        self.graph = pandas.DataFrame(columns=Sensors.ALL)

    def add(self, rows):
        self.graph = self.graph.append(rows, ignore_index=True)


realtime = RealtimeData()

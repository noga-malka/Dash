import pandas

from consts import DataConsts


class RealtimeData:
    def __init__(self):
        self.graph = pandas.DataFrame(columns=[DataConsts.TIME, DataConsts.SENSOR, DataConsts.VALUE])

    def add(self, rows):
        self.graph = self.graph.append(rows, ignore_index=True)


realtime = RealtimeData()

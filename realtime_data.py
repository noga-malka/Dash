import datetime

import pandas

from consts import DataConsts


class RealtimeData:
    def __init__(self):
        self.graph = None
        self.clear_session()

    def add(self, rows):
        self.graph = self.graph.append(rows, ignore_index=True)

    def save_session(self):
        data = self.graph.pivot(columns='sensor', index='time').droplevel(0, axis=1)
        data.to_csv(f'output/data_{datetime.datetime.now().strftime("%Y_%m_%d %H-%M-%S")}.csv')

    def clear_session(self):
        self.graph = pandas.DataFrame(columns=[DataConsts.TIME, DataConsts.SENSOR, DataConsts.VALUE])


realtime = RealtimeData()

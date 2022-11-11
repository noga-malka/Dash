import datetime

import pandas

from consts import TagIds


class RealtimeData:
    def __init__(self):
        self.graph = None
        self.index = None
        self.is_paused = False
        self.clean()
        self.config = {
            'to-start': lambda: self.set_index(0),
            'forward': lambda: self.step(TagIds.Icons.GAP),
            'pause': self.pause,
            'play': self.play,
            'clean': self.clean,
            'save': self.save,
            'backward': lambda: self.step(-TagIds.Icons.GAP),
            'to-end': lambda: self.set_index()
        }

    def set_index(self, value=-1):
        self.index = value

    def step(self, gap: int):
        if self.index == -1:
            self.index = len(self.graph) - 1
        new_index = self.index + gap
        self.index = max(0, new_index) if gap < 0 else min(len(self.graph) - 1, new_index)

    def go_to_start(self):
        self.index = 0

    def pause(self):
        self.is_paused = True
        self.index = len(self.graph) - 1 if self.index == -1 else self.index

    def play(self):
        self.is_paused = False

    def go_to_end(self):
        self.index = -1

    def read_data(self, step=1):
        current = self.graph.iloc[self.index]
        if self.index != -1 and not self.is_paused:
            self.index += step
        return current

    def add(self, rows):
        self.graph = pandas.concat([realtime.graph, rows])

    def save(self):
        self.graph.to_csv(f'output/data_{datetime.datetime.now().strftime("%Y_%m_%d %H-%M-%S")}.csv')

    def clean(self):
        self.go_to_end()
        self.graph = pandas.DataFrame()

    def load_data(self, data):
        self.graph = data
        self.go_to_start()


realtime = RealtimeData()

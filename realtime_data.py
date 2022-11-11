import datetime

import pandas


class RealtimeData:
    def __init__(self):
        self.graph = None
        self.index = None
        self.is_paused = False
        self.clean()
        self.config = {
            'to-start': self.go_to_start,
            'pause': self.pause,
            'play': self.play,
            'clean': self.clean,
            'save': self.save,
            'to-end': self.go_to_end
        }

    def go_to_start(self):
        self.index = 0

    def pause(self):
        self.is_paused = True
        self.index = len(self.graph) - 1

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

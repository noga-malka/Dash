import pandas

from consts import RealtimeConsts
from stoppable_thread import StoppableThread, types


class RealtimeData:
    def __init__(self):
        self.thread = StoppableThread(target=self.add_data, daemon=True)
        self.thread.start()
        self.graph = pandas.DataFrame()
        self.index = -1
        self.is_paused = False
        self.should_clean = False
        self.config = {
            'to-start': lambda: self.set_index(0),
            'forward': lambda: self.step(RealtimeConsts.GAP),
            'pause': self.pause,
            'play': self.play,
            'backward': lambda: self.step(-RealtimeConsts.GAP),
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
        self.thread.events.Finish.connect.clear()

    def play(self):
        self.is_paused = False
        self.thread.events.Finish.connect.set()

    def go_to_end(self):
        self.index = -1

    def read_data(self, step=RealtimeConsts.STEP):
        current = self.graph.iloc[self.index]
        if self.index != -1 and not self.is_paused:
            self.index += step
        return current.astype(int)

    def add_data(self):
        if self.thread.events.clean.is_set():
            self.graph = pandas.DataFrame()
            self.thread.events.Finish.clean.set()
        else:
            self.graph = pandas.concat([self.graph, types[self.thread.handler_name].extract_data()])

    def clean(self):
        self.thread.events.clean.set()


realtime = RealtimeData()

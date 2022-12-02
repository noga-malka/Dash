import datetime

import pandas

from consts import RealtimeConsts
from handlers.bluethooth_reader import BluetoothHandler
from handlers.random_handler import RandomHandler
from handlers.serial_reader import SerialHandler
from stoppable_thread import StoppableThread

types = {'serial': SerialHandler(), 'bluetooth': BluetoothHandler(), 'random': RandomHandler()}


class RealtimeData:
    def __init__(self):
        self.handler_name = 'random'
        self.handler = None
        self.thread = None
        self.graph = pandas.DataFrame()
        self.index = -1
        self.is_paused = False
        self.should_clean = False
        self.config = {
            'to-start': lambda: self.set_index(0),
            'forward': lambda: self.step(RealtimeConsts.GAP),
            'pause': self.pause,
            'play': self.play,
            'clean': self.clean,
            'save': self.save,
            'backward': lambda: self.step(-RealtimeConsts.GAP),
            'to-end': lambda: self.set_index()
        }

    def set_handler(self, handler=''):
        self.handler_name = handler
        self.handler = types.get(self.handler_name, types['random'])

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

    def read_data(self, step=RealtimeConsts.STEP):
        current = self.graph.iloc[self.index]
        if self.index != -1 and not self.is_paused:
            self.index += step
        return current.astype(int)

    def add_data(self):
        if self.should_clean:
            self.should_clean = False
            self.graph = pandas.DataFrame()
        else:
            self.graph = pandas.concat([self.graph, self.handler.extract_data()])

    def read_setup(self):
        self.handler.is_connected = self.handler.connect()
        return self.add_data

    def start_loop(self):
        self.thread = StoppableThread(setup=self.read_setup, daemon=True, cleanup=self.clean)
        self.thread.start()

    def save(self):
        self.graph.to_csv(f'output/data_{datetime.datetime.now().strftime("%Y_%m_%d %H-%M-%S")}.csv')

    def clean(self):
        self.should_clean = True

    def load_data(self, data):
        self.graph = data
        self.go_to_start()


realtime = RealtimeData()

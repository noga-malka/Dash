import functools

import pandas


class Dataframe:
    def __init__(self):
        self.data = None
        self.single_values = None
        self._mapping = {
            'single': self.save_single_value,
            'row': self.add_row,
            'frame': self.merge,
            'ignore': lambda args: None,
        }
        self.reset()

    def save(self, current_data: dict):
        for data_type, args in current_data.items():
            self._mapping[data_type](args)

    def reset(self, event=None):
        self.data = pandas.DataFrame()
        self.single_values = {}
        if event:
            event.set()

    def is_not_empty(self):
        return len(self.data)

    def time_gap(self):
        total = pandas.Timestamp(self.read_row().name) - pandas.Timestamp(self.read_row(0).name)
        return str(total).split(' ')[-1]

    def read_row(self, index=-1):
        return self.data.iloc[index]

    def save_single_value(self, values):
        for (key, value, event) in values:
            self.single_values[key] = value
            if event:
                event.set()

    def get(self, key, default_value=None):
        return self.single_values.get(key, default_value)

    def set(self, key, value):
        self.single_values[key] = value

    def merge(self, dataframes):
        dataframes = list(filter(lambda data: not data.empty, dataframes))
        if dataframes:
            self.data = pandas.concat([self.data, *dataframes])

    def add_row(self, content):
        row = pandas.DataFrame(functools.reduce(lambda a, b: a | b, content, {}), index=[pandas.Timestamp.now()])
        if not row.empty:
            self.data = self.data.append(row)

    def to_csv(self, path=None):
        return self.data.to_csv(path)

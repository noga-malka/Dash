import functools
import re

import pandas

from consts import DatabaseTypes, DatabaseReader


class DatabaseManager:
    def __init__(self):
        self.data = None
        self.single_values = None
        self._mapping = {
            DatabaseTypes.SINGLE_VALUE: self.save_single_value,
            DatabaseTypes.ROW: self.add_row,
            DatabaseTypes.DATAFRAME: self.merge,
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
        total = pandas.Timestamp(self.read().name) - pandas.Timestamp(self.read(DatabaseReader.FIRST).name)
        return re.search('([0-9]{2}|:)+', str(total)).group(0)

    def read(self, index=DatabaseReader.LAST):
        return self.data if index == DatabaseReader.ALL else self.data.iloc[index.value]

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
        if not row.empty and len(row.columns) >= len(self.data.columns):
            self.data = self.data.append(row)

    def to_csv(self, path=None):
        return self.data.to_csv(path)

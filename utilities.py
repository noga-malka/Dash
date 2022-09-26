import pandas

from consts import DataConsts
from realtime_data import realtime
from serial_reader import SerialHandler


def save_serial_data(handler: SerialHandler):
    while True:
        try:
            data = handler.read_line().strip().split('\t')
            current_time = pandas.Timestamp.now()
            sample = [
                {DataConsts.TIME: current_time, DataConsts.SENSOR: data[index],
                 DataConsts.VALUE: float(data[index + 1])}
                for index in range(0, len(data), 2)]
            realtime.add(sample)
        except (KeyError, IndexError):
            pass

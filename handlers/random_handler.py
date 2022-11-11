import random
import time

from configurations import Settings
from handlers.handler import Handler


class RandomHandler(Handler):
    def __init__(self):
        super(RandomHandler, self).__init__()

    def connect(self):
        return True

    def read_line(self) -> str:
        time.sleep(0.5)
        values = [[name, str(random.randint(sensor.minimum, sensor.maximum))] for name, sensor in
                  Settings.SENSORS.items()]
        return "\t".join(sum(values, []))

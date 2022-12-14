import dash_daq as daq

from consts import UnitTypes
from monitors.basic_monitor import Monitor


class TemperatureMonitor(Monitor):

    def generate_daq(self, monitor_id):
        change_function = UnitTypes.CONVERT[self.sensor.unit_type]
        temp = daq.Thermometer(id=monitor_id, label=self.sensor.label, value=self.sensor.minimum,
                               showCurrentValue=True, units=self.sensor.unit_type,
                               min=change_function(self.sensor.minimum), max=change_function(self.sensor.maximum),
                               height=self.size, width=self.size / 10)
        return [temp, self.generate_led(monitor_id)]

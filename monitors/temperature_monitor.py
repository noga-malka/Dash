import dash_daq as daq

from consts import UnitTypes
from monitors.basic_monitor import Monitor


class TemperatureMonitor(Monitor):

    def generate_daq(self, sensor, monitor_id):
        change_function = UnitTypes.get_converter(sensor.unit_type)
        temp = daq.Thermometer(id=monitor_id, label=sensor.label, value=sensor.minimum,
                               showCurrentValue=True, units=sensor.unit_type,
                               min=change_function(sensor.minimum), max=change_function(sensor.maximum),
                               height=self.size, width=self.size / 10)
        return [temp, self.generate_led(sensor, monitor_id)]

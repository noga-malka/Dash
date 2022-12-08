import dash_daq as daq

from monitors.basic_monitor import Monitor


class TemperatureMonitor(Monitor):

    def generate_daq(self, monitor_id):
        temp = daq.Thermometer(id=monitor_id, label=self.sensor.label, value=self.sensor.minimum,
                               showCurrentValue=True, units=self.sensor.unit_type,
                               min=self.sensor.minimum, max=self.sensor.maximum,
                               height=self.size, width=self.size / 10)
        return [temp, self.generate_led(monitor_id)]

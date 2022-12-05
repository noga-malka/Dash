import dash_daq as daq

from monitors.basic_monitor import Monitor


class GaugeMonitor(Monitor):

    def __init__(self, sensor, size, units=None, show_label=True):
        super(GaugeMonitor, self).__init__(sensor, size, show_label)
        self.units = units
        if show_label:
            self.extra_kwargs['label'] = self.sensor.label

    def generate_daq(self, monitor_id):
        gauge = daq.Gauge(id=monitor_id, value=self.sensor.minimum, size=self.size, units=self.units,
                          showCurrentValue=True, min=self.sensor.minimum, max=self.sensor.maximum, **self.extra_kwargs)
        return [gauge, self.generate_led(monitor_id)]

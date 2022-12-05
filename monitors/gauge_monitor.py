import dash_daq as daq
from dash import html, Output

from consts import Colors
from monitors.basic_monitor import Monitor


class GaugeMonitor(Monitor):

    def __init__(self, sensor, size, units=None, show_label=True, show_percentage=False, max_percent=None):
        super(GaugeMonitor, self).__init__(sensor, size, units, show_label)
        self.show_percentage = show_percentage
        self.max_percent = max_percent
        if show_label:
            self.extra_kwargs['label'] = self.sensor.label

    def generate_daq(self, monitor_id):
        gauge = daq.Gauge(id=monitor_id, value=self.sensor.minimum, size=self.size, units=self.units,
                          showCurrentValue=True, min=self.sensor.minimum, max=self.sensor.maximum, **self.extra_kwargs)
        led = self.generate_led(monitor_id)
        if self.show_percentage:
            led = html.Div([led, self.generate_led(monitor_id + '_percent', color=Colors.GOOD, is_valid=True)],
                           style={'width': 'inherit', 'display': 'flex', 'justify-content': 'space-around'})
        return [gauge, led]

    def generate_output_values(self, value):
        values = super(GaugeMonitor, self).generate_output_values(value)
        if self.show_percentage:
            percent = value / self.max_percent * 100 if self.max_percent else -1
            extra = ['{:.2f}'.format(percent)] + values[-2:]
            values += extra
        return values

    def generate_output_list(self, sensor_key):
        output_list = super(GaugeMonitor, self).generate_output_list(sensor_key)
        if self.show_percentage:
            extra = [Output(sensor_key + '_percent_led', 'value'), Output(sensor_key + '_percent_led', 'color'),
                     Output(sensor_key + '_percent_icon', 'className')]
            output_list.append(extra)
        return output_list

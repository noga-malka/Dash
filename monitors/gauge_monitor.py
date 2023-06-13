import dash_daq as daq
from dash import html, Output

from monitors.basic_monitor import Monitor


class GaugeMonitor(Monitor):

    def __init__(self, size, show_label=True, show_percentage=False, max_percent=None, adapt_function=None):
        super(GaugeMonitor, self).__init__(size, show_label)
        self.show_percentage = show_percentage
        self.max_percent = max_percent
        self.show_label = show_label
        self.adapt_function = adapt_function if adapt_function else lambda value: value

    def generate_daq(self, sensor, monitor_id):
        if self.show_label:
            self.extra_kwargs['label'] = sensor.label
        gauge = daq.Gauge(id=monitor_id, value=sensor.minimum, size=self.size, units=sensor.unit_type,
                          showCurrentValue=True, min=sensor.minimum, max=sensor.maximum, **self.extra_kwargs)
        led = self.generate_led(sensor, monitor_id)
        if self.show_percentage:
            led = html.Div([led, self.generate_led(sensor, monitor_id + '_percent', label='%')],
                           style={'width': 'inherit', 'display': 'flex', 'justify-content': 'space-around'})
        return [gauge, led]

    def generate_output_values(self, sensor, value):
        values = super(GaugeMonitor, self).generate_output_values(sensor, self.adapt_function(value))
        if self.show_percentage:
            percent = value / self.max_percent * 100 if self.max_percent else -1
            values.append(['{:.2f}'.format(percent)] + values[-2:])
        return values

    def generate_output_list(self, sensor_key):
        output_list = super(GaugeMonitor, self).generate_output_list(sensor_key)
        if self.show_percentage:
            extra = [Output(sensor_key + '_percent_led', 'value'), Output(sensor_key + '_percent_led', 'color'),
                     Output(sensor_key + '_percent_icon', 'className')]
            output_list.append(extra)
        return output_list

import dash_daq as daq
from dash import html, Output

from consts import TagIds


class Monitor:
    def __init__(self, sensor, size, units=None, show_label=False):
        self.size = size
        self.sensor = sensor
        self.show_label = show_label
        self.units = units
        self.extra_kwargs = {}

    def generate_daq(self, monitor_id):
        raise NotImplementedError

    def generate_output_list(self, sensor_key):
        return [Output(sensor_key, 'value'), Output(sensor_key, 'color'), Output(sensor_key + '_led', 'value'),
                Output(sensor_key + '_led', 'color'), Output(sensor_key + '_icon', 'className')]

    def generate_output_values(self, value):
        is_valid = self.sensor.low < value < self.sensor.high
        icon = f'{TagIds.Icons.CHECK} valid' if is_valid else f'{TagIds.Icons.WARNING} invalid'
        color = '#ABE2FB' if is_valid else 'red'
        return [value, color, value, color, f'fa {icon}']

    def generate_led(self, led_id):
        icon = html.Div(id=led_id + '_icon', className=f'fa {TagIds.Icons.WARNING} invalid')
        return html.Div(
            [icon, daq.LEDDisplay(id=led_id + '_led', value=self.sensor.minimum, size=20, color='red')],
            className='center align children-margin-2')

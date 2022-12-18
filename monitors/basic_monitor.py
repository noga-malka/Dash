import dash_daq as daq
import numpy
from dash import html, Output

from consts import Colors, ValueRange, UnitTypes


class Monitor:
    def __init__(self, sensor, size, show_label=False):
        self.size = size
        self.sensor = sensor
        self.show_label = show_label
        self.extra_kwargs = {}

    def generate_daq(self, monitor_id):
        raise NotImplementedError

    def generate_output_list(self, sensor_key):
        return [Output(sensor_key, 'value'), Output(sensor_key, 'color'), Output(sensor_key + '_led', 'value'),
                Output(sensor_key + '_led', 'color'), Output(sensor_key + '_icon', 'className')]

    @staticmethod
    def _get_icon(level):
        return f'fa {ValueRange.ICONS[level]} fa-lg'

    def generate_output_values(self, value):
        sensor_dict = self.sensor.dict()
        current_level = Colors.ERROR
        if numpy.isnan(value):
            current_level = Colors.DISCONNECTED
        else:
            for (minimum, maximum), level in ValueRange.LEVEL_COMPARE.items():
                if sensor_dict[minimum] <= value <= sensor_dict[maximum]:
                    current_level = level
        value = UnitTypes.CONVERT[self.sensor.unit_type](value)
        return [value, current_level.value, value, current_level.value, self._get_icon(current_level)]

    def generate_led(self, led_id, label=None):
        icon = html.Div(id=led_id + '_icon', className=self._get_icon(Colors.WARNING))
        label = label if label else self.sensor.unit_type
        return html.Div([icon, daq.LEDDisplay(id=led_id + '_led', value=self.sensor.minimum, label=label,
                                              labelPosition='bottom', size=25, color=Colors.ERROR.value)],
                        className='flex center align children-margin-2')

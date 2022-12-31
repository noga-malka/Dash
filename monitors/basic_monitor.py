import dash_daq as daq
import numpy
from dash import html, Output

from consts import Colors, ValueRange, UnitTypes


class Monitor:
    def __init__(self, size, show_label=False):
        self.size = size
        self.show_label = show_label
        self.extra_kwargs = {}

    def generate_daq(self, sensor, monitor_id):
        raise NotImplementedError

    def generate_output_list(self, sensor_key):
        return [Output(sensor_key, 'value'), Output(sensor_key, 'color'), Output(sensor_key + '_led', 'value'),
                Output(sensor_key + '_led', 'color'), Output(sensor_key + '_icon', 'className')]

    @staticmethod
    def _get_icon(level):
        return f'fa {ValueRange.ICONS[level]} fa-lg'

    def generate_output_values(self, sensor, value):
        sensor_dict = sensor.dict()
        current_level = Colors.ERROR
        if numpy.isnan(value):
            current_level = Colors.DISCONNECTED
        else:
            for (minimum, maximum), level in ValueRange.LEVEL_COMPARE.items():
                if sensor_dict[minimum] <= value <= sensor_dict[maximum]:
                    current_level = level
            value = UnitTypes.CONVERT[sensor.unit_type](value)
        return [value, current_level.value, '{:.2f}'.format(value), current_level.value, self._get_icon(current_level)]

    def generate_led(self, sensor, led_id, label=None):
        icon = html.Div(id=led_id + '_icon', className=self._get_icon(Colors.WARNING))
        label = label if label else sensor.unit_type
        return html.Div([icon, daq.LEDDisplay(id=led_id + '_led', value=sensor.minimum, label=label,
                                              labelPosition='bottom', size=20, color=Colors.ERROR.value)],
                        className='flex center align children-margin-2')

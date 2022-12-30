import dash_daq as daq
from dash import html

from monitors.basic_monitor import Monitor


class SliderMonitor(Monitor):

    def generate_daq(self, sensor, monitor_id):
        label = html.Label(sensor.label, className='label-style')
        slider = daq.Slider(id=monitor_id, handleLabel=sensor.label,
                            value=sensor.minimum, targets={},
                            max=sensor.maximum, min=sensor.minimum, size=self.size, disabled=True)
        return [label, slider, self.generate_led(sensor, monitor_id)]

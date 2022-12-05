import dash_daq as daq
from dash import html

from monitors.basic_monitor import Monitor


class SliderMonitor(Monitor):

    def generate_daq(self, monitor_id):
        label = html.Label(self.sensor.label, className='label-style')
        slider = daq.Slider(id=monitor_id, handleLabel=self.sensor.label,
                            value=self.sensor.minimum, targets={},
                            max=self.sensor.maximum, min=self.sensor.minimum, size=self.size, disabled=True)
        return [label, slider, self.generate_led(monitor_id)]

import dash_daq as daq
from dash import html

from configurations import Sensor, Settings


def generate_slider(monitor_id, size, sensor):
    label = html.Label(sensor.label, className='label-style')
    slider = daq.Slider(id=monitor_id, handleLabel=sensor.label,
                        value=sensor.minimum, targets={str(sensor.low): 'low', str(sensor.high): 'high'},
                        max=sensor.maximum, min=sensor.minimum, size=size, disabled=True)
    return [label, slider]


def generate_led(monitor_id, size, sensor):
    return [daq.LEDDisplay(id=monitor_id + '_led', value=sensor.minimum, size=size, color='red')]


def generate_thermometer(monitor_id, size, sensor):
    return [
        daq.Thermometer(id=monitor_id, label=sensor.label, value=sensor.minimum, min=sensor.minimum, max=sensor.maximum,
                        height=size, width=size / 10)]


def generate_gauge(monitor_id, size, sensor):
    return [daq.Gauge(id=monitor_id, label=sensor.label, value=sensor.minimum, size=size,
                      min=sensor.minimum, max=sensor.maximum)]


mapping = {
    'slider': generate_slider,
    'gauge': generate_gauge,
    'thermometer': generate_thermometer,
}


def generate_monitor(field, sensor: Sensor):
    monitor_type, size = Settings.TYPES[sensor.label]
    return mapping[monitor_type](field, size, sensor) + generate_led(field, Settings.LED_SIZE, sensor)

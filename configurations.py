import functools
import logging.config

from pydantic import Field, BaseModel

from monitors.gauge_monitor import GaugeMonitor
from monitors.temperature_monitor import TemperatureMonitor

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('caeli')


class Sensor(BaseModel):
    label: str = Field(..., editable=False, content_type='text')
    minimum: int = Field(..., content_type='numeric')
    low_error: int = Field(..., content_type='numeric')
    low_warning: int = Field(..., content_type='numeric')
    high_warning: int = Field(..., content_type='numeric')
    high_error: int = Field(..., content_type='numeric')
    maximum: int = Field(..., content_type='numeric')
    unit_type: str = Field(..., editable=False, content_type='text')


class Settings:
    CO2 = Sensor(label='CO2', minimum=0, low_error=0, low_warning=0, high_warning=6000, high_error=8000, maximum=10000,
                 unit_type='PPM')
    Temperature = Sensor(label='Temperature', minimum=10, low_error=20, low_warning=25, high_warning=35, high_error=40,
                         maximum=50, unit_type='C°')
    Humidity = Sensor(label='Humidity', minimum=0, low_error=10, low_warning=20, high_warning=80, high_error=90,
                      maximum=100, unit_type='%')
    ALL_SENSORS = [CO2, Temperature, Humidity]

    TYPES = {
        CO2.label: GaugeMonitor(CO2, 210, show_label=False, show_percentage=True, max_percent=1000000),
        Temperature.label: TemperatureMonitor(Temperature, 150),
        Humidity.label: GaugeMonitor(Humidity, 160),
    }
    LED_SIZE = 20

    GROUPS = {
        'CO2 sensor': {
            'CO2 sensor CO2': CO2,
            'CO2 sensor Hum': Humidity,
            'CO2 sensor Temp': Temperature,
        },
        'HTU21DF-1 sensor': {
            'HTU21DF-1 sensor Humidity': Humidity,
            'HTU21DF-1 sensor Temp': Temperature,
        },
        'HTU21DF-2 sensor': {
            'HTU21DF-2 sensor Humidity': Humidity,
            'HTU21DF-2 sensor Temp': Temperature,
        },
        'DS18B20-1 sensor': {
            'DS18B20-1 sensor Temp': Temperature,
        },
        'DS18B20-2 sensor': {
            'DS18B20-2 sensor Temp': Temperature
        }
    }
    GRAPHS = {
        'Temperature': [
            'CO2 sensor Temp',
            'HTU21DF-1 sensor Temp',
            'HTU21DF-2 sensor Temp',
            'DS18B20-1 sensor Temp',
            'DS18B20-2 sensor Temp'
        ],
        'Humidity': [
            'CO2 sensor Hum',
            'HTU21DF-1 sensor Humidity',
            'HTU21DF-2 sensor Humidity',
        ],
        'CO2': [
            'CO2 sensor CO2',
        ],
    }
    SENSORS = functools.reduce(lambda x, y: x | y, GROUPS.values(), {})

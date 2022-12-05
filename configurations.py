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
    low: int = Field(..., content_type='numeric')
    high: int = Field(..., content_type='numeric')
    maximum: int = Field(..., content_type='numeric')


class Settings:
    CO2 = Sensor(label='CO2', minimum=0, low=200, high=7000, maximum=10000)
    Temperature = Sensor(label='Temperature', minimum=20, low=28, high=32, maximum=35)
    Humidity = Sensor(label='Humidity', minimum=0, low=10, high=90, maximum=100)
    ALL_SENSORS = [CO2, Temperature, Humidity]

    TYPES = {
        CO2.label: GaugeMonitor(CO2, 210, "PPM", False),
        Temperature.label: TemperatureMonitor(Temperature, 150, 'C°'),
        Humidity.label: GaugeMonitor(Humidity, 160, '%'),
    }
    LED_SIZE = 20

    GROUPS = {
        'CO2 sensor': {
            'CO2 sensor CO2': CO2,
        },
        'CO2 extra sensors': {
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

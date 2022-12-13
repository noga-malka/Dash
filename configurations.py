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
    possible_units: list[str] = Field(..., editable=False, hidden=True)


class SensorInstance:
    CO2 = Sensor(label='CO2',
                 minimum=0,
                 low_error=0,
                 low_warning=0,
                 high_warning=6000,
                 high_error=8000,
                 maximum=10000,
                 unit_type='PPM',
                 possible_units=['PPM'])

    Temperature = Sensor(label='Temperature',
                         minimum=10,
                         low_error=20,
                         low_warning=25,
                         high_warning=35,
                         high_error=40,
                         maximum=50,
                         unit_type='C°',
                         possible_units=['C°', 'F°'])

    Humidity = Sensor(label='Humidity',
                      minimum=0,
                      low_error=10,
                      low_warning=20,
                      high_warning=80,
                      high_error=90,
                      maximum=100,
                      unit_type='%',
                      possible_units=['%'])


class Schema:
    ALL = [SensorInstance.CO2, SensorInstance.Temperature, SensorInstance.Humidity]
    SENSOR_SCHEMA = Sensor.schema()['properties']
    HIDDEN_FIELDS = {key for key, field in Sensor.schema()['properties'].items() if field.get('hidden')}

    MONITOR_TYPES = {
        SensorInstance.CO2.label: GaugeMonitor(SensorInstance.CO2, 210, False, True, max_percent=1000000),
        SensorInstance.Temperature.label: TemperatureMonitor(SensorInstance.Temperature, 150),
        SensorInstance.Humidity.label: GaugeMonitor(SensorInstance.Humidity, 160),
    }


class Settings:
    GROUPS = {
        'CO2 sensor': {
            'CO2 sensor CO2': SensorInstance.CO2,
            'CO2 sensor Hum': SensorInstance.Humidity,
            'CO2 sensor Temp': SensorInstance.Temperature,
        },
        'HTU21DF-1 sensor': {
            'HTU21DF-1 sensor Humidity': SensorInstance.Humidity,
            'HTU21DF-1 sensor Temp': SensorInstance.Temperature,
        },
        'HTU21DF-2 sensor': {
            'HTU21DF-2 sensor Humidity': SensorInstance.Humidity,
            'HTU21DF-2 sensor Temp': SensorInstance.Temperature,
        },
        'DS18B20-1 sensor': {
            'DS18B20-1 sensor Temp': SensorInstance.Temperature,
        },
        'DS18B20-2 sensor': {
            'DS18B20-2 sensor Temp': SensorInstance.Temperature
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

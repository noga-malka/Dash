import functools
import logging.config

from pydantic import Field, BaseModel

from monitors.gauge_monitor import GaugeMonitor
from monitors.temperature_monitor import TemperatureMonitor

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('caeli')

logging.getLogger('werkzeug').setLevel(logging.ERROR)

class Sensor(BaseModel):
    label: str = Field(..., editable=False, content_type='text')
    minimum: float = Field(..., content_type='numeric')
    low_error: float = Field(..., content_type='numeric')
    low_warning: float = Field(..., content_type='numeric')
    high_warning: float = Field(..., content_type='numeric')
    high_error: float = Field(..., content_type='numeric')
    maximum: float = Field(..., content_type='numeric')
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
                         high_error=38,
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

    Pressure = Sensor(label='Pressure',
                      minimum=0,
                      low_error=0.5,
                      low_warning=0.8,
                      high_warning=1.2,
                      high_error=1.5,
                      maximum=2,
                      unit_type='PSI',
                      possible_units=['PSI'])


class Schema:
    ALL = [SensorInstance.CO2, SensorInstance.Temperature, SensorInstance.Humidity, SensorInstance.Pressure]
    SENSOR_SCHEMA = Sensor.schema()['properties']
    HIDDEN_FIELDS = {key for key, field in Sensor.schema()['properties'].items() if field.get('hidden')}

    MONITOR_TYPES = {
        SensorInstance.CO2.label: GaugeMonitor(SensorInstance.CO2, 210, False, True, max_percent=1000000),
        SensorInstance.Temperature.label: TemperatureMonitor(SensorInstance.Temperature, 150),
        SensorInstance.Humidity.label: GaugeMonitor(SensorInstance.Humidity, 160),
        SensorInstance.Pressure.label: GaugeMonitor(SensorInstance.Pressure, 160),
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
        'DS18B20-1 sensor': {
            'DS18B20-1 sensor Temp': SensorInstance.Temperature,
        },
        'DS18B20-2 sensor': {
            'DS18B20-2 sensor Temp': SensorInstance.Temperature
        },
        'DS18B20-3 sensor': {
            'DS18B20-3 sensor Temp': SensorInstance.Temperature
        },
        'DS18B20-4 sensor': {
            'DS18B20-4 sensor Temp': SensorInstance.Temperature
        },
        'Pressure-1 sensor': {
            'pressure-1 sensor': SensorInstance.Pressure
        },
        'Pressure-2 sensor': {
            'pressure-2 sensor': SensorInstance.Pressure
        }
    }
    CARD_ORDER = [
        ['CO2 sensor', 'HTU21DF-1 sensor'],
        ['DS18B20-1 sensor', 'DS18B20-2 sensor', 'DS18B20-3 sensor', 'DS18B20-4 sensor'],
        ['Pressure-1 sensor', 'Pressure-2 sensor'],
    ]
    GRAPHS = {
        'Temperature': [
            'CO2 sensor Temp',
            'HTU21DF-1 sensor Temp',
            'DS18B20-1 sensor Temp',
            'DS18B20-2 sensor Temp'
        ],
        'Humidity': [
            'CO2 sensor Hum',
            'HTU21DF-1 sensor Humidity',
        ],
        'CO2': [
            'CO2 sensor CO2',
        ],
    }
    SENSORS = functools.reduce(lambda x, y: x | y, GROUPS.values(), {})

import functools
import logging.config

from pydantic import Field, BaseModel

from monitors.gauge_monitor import GaugeMonitor
from monitors.temperature_monitor import TemperatureMonitor

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('caeli')

logging.getLogger('werkzeug').propagate = False


class InputNames:
    CO2 = 'CO2 sensor CO2'
    CO2_HUMIDITY = 'CO2 sensor Hum'
    CO2_TEMP = 'CO2 sensor Temp'
    HTU_HUMIDITY = 'HTU21DF-1 sensor Humidity'
    HTU_TEMP = 'HTU21DF-1 sensor Temp'
    DS_TEMP_1 = 'DS18B20-1 sensor Temp'
    DS_TEMP_2 = 'DS18B20-2 sensor Temp'
    DS_TEMP_3 = 'DS18B20-3 sensor Temp'
    DS_TEMP_4 = 'DS18B20-4 sensor Temp'
    PRESSURE_1 = 'pressure 1'
    PRESSURE_2 = 'pressure 2'


class SensorNames:
    CO2 = 'CO2 sensor'
    HTU = 'HTU21DF-1 sensor'
    DS1 = 'DS18B20-1 sensor'
    DS2 = 'DS18B20-2 sensor'
    DS3 = 'DS18B20-3 sensor'
    DS4 = 'DS18B20-4 sensor'
    PRESSURE1 = 'Pressure-1'
    PRESSURE2 = 'Pressure-2'


class Sensor(BaseModel):
    name: str = Field('', editable=False, content_type='text')
    label: str = Field(..., editable=False, content_type='text')
    minimum: float = Field(..., content_type='numeric')
    low_error: float = Field(..., content_type='numeric')
    low_warning: float = Field(..., content_type='numeric')
    high_warning: float = Field(..., content_type='numeric')
    high_error: float = Field(..., content_type='numeric')
    maximum: float = Field(..., content_type='numeric')
    unit_type: str = Field(..., editable=False, content_type='text')
    possible_units: list[str] = Field(..., editable=False, hidden=True)


class Labels:
    CO2 = 'CO2'
    TEMP = 'Temperature'
    HUMIDITY = 'Humidity'
    PRESSURE = 'Pressure'


class SensorInstance:
    CO2 = Sensor(label=Labels.CO2,
                 minimum=0,
                 low_error=0,
                 low_warning=0,
                 high_warning=6000,
                 high_error=8000,
                 maximum=10000,
                 unit_type='PPM',
                 possible_units=['PPM'])

    Temperature = Sensor(label=Labels.TEMP,
                         minimum=10,
                         low_error=20,
                         low_warning=25,
                         high_warning=35,
                         high_error=38,
                         maximum=50,
                         unit_type='C°',
                         possible_units=['C°', 'F°'])

    Humidity = Sensor(label=Labels.HUMIDITY,
                      minimum=0,
                      low_error=10,
                      low_warning=20,
                      high_warning=80,
                      high_error=90,
                      maximum=100,
                      unit_type='%',
                      possible_units=['%'])

    Pressure = Sensor(label=Labels.PRESSURE,
                      minimum=0,
                      low_error=0.5,
                      low_warning=0.8,
                      high_warning=1.2,
                      high_error=1.5,
                      maximum=2,
                      unit_type='PSI',
                      possible_units=['PSI'])


class Schema:
    SENSOR_SCHEMA = Sensor.schema()['properties']
    HIDDEN_FIELDS = {key for key, field in SENSOR_SCHEMA.items() if field.get('hidden')}

    MONITOR_TYPES = {
        Labels.CO2: GaugeMonitor(210, False, True, max_percent=1000000),
        Labels.TEMP: TemperatureMonitor(150),
        Labels.HUMIDITY: GaugeMonitor(160),
        Labels.PRESSURE: GaugeMonitor(160),
    }


def parse_sensors(groups):
    for group_name, group in groups.items():
        for key, sensor in group.items():
            current = group[key].copy()
            current.name = group_name
            group[key] = current
    return functools.reduce(lambda x, y: x | y, groups.values(), {})


class Settings:
    GROUPS = {
        SensorNames.CO2: {
            InputNames.CO2: SensorInstance.CO2,
            InputNames.CO2_HUMIDITY: SensorInstance.Humidity,
            InputNames.CO2_TEMP: SensorInstance.Temperature,
        },
        SensorNames.HTU: {
            InputNames.HTU_HUMIDITY: SensorInstance.Humidity,
            InputNames.HTU_TEMP: SensorInstance.Temperature,
        },
        SensorNames.DS1: {
            InputNames.DS_TEMP_1: SensorInstance.Temperature,
        },
        SensorNames.DS2: {
            InputNames.DS_TEMP_2: SensorInstance.Temperature
        },
        SensorNames.DS3: {
            InputNames.DS_TEMP_3: SensorInstance.Temperature
        },
        SensorNames.DS4: {
            InputNames.DS_TEMP_4: SensorInstance.Temperature
        },
        SensorNames.PRESSURE1: {
            InputNames.PRESSURE_1: SensorInstance.Pressure
        },
        SensorNames.PRESSURE2: {
            InputNames.PRESSURE_2: SensorInstance.Pressure
        }
    }
    CARD_ORDER = [
        [SensorNames.CO2, SensorNames.HTU],
        [SensorNames.DS1, SensorNames.DS2, SensorNames.DS3, SensorNames.DS4],
        [SensorNames.PRESSURE1, SensorNames.PRESSURE2],
    ]
    GRAPHS = {
        'CO2': [
            InputNames.CO2,
        ],
        'Temperature': [
            InputNames.CO2_TEMP,
            InputNames.HTU_TEMP,
            InputNames.DS_TEMP_1,
            InputNames.DS_TEMP_2,
            InputNames.DS_TEMP_3,
            InputNames.DS_TEMP_4,
        ],
        'Humidity': [
            InputNames.CO2_HUMIDITY,
            InputNames.HTU_HUMIDITY,
        ],
    }
    SENSORS = parse_sensors(GROUPS)


class SetupConsts:
    DS_TEMP = [sensor for name, sensor in Settings.SENSORS.items() if
               name in [InputNames.DS_TEMP_1, InputNames.DS_TEMP_2, InputNames.DS_TEMP_3, InputNames.DS_TEMP_4]]
    COMMANDS = {
        SensorNames.DS1: 18, SensorNames.DS2: 19, SensorNames.DS3: '1a', SensorNames.DS4: '1b'
    }

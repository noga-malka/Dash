import logging.config

from pydantic import Field, BaseModel

from consts import IS_DEBUG, UnitTypes
from monitors.gauge_monitor import GaugeMonitor
from monitors.temperature_monitor import TemperatureMonitor

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('caeli')

logging.getLogger('werkzeug').disabled = not IS_DEBUG
logging.getLogger('callbacks').disabled = not IS_DEBUG


class InputNames:
    CO2 = 'CO2 sensor CO2'
    CO2_HUMIDITY = 'CO2 sensor Hum'
    CO2_TEMP = 'CO2 sensor Temp'
    HTU_HUMIDITY = 'HTU21DF-1 sensor Humidity'
    HTU_TEMP = 'HTU21DF-1 sensor Temp'
    DS_TEMP_1 = 'Mouth Temp'
    DS_TEMP_2 = 'Lungs Temp'
    DS_TEMP_3 = 'Canister Top Temp'
    DS_TEMP_4 = 'Canister Bottom Temp'
    PRESSURE_1 = 'pressure 1'
    PRESSURE_2 = 'pressure 2'
    PRESSURE_1_TEMP = 'Temp pressure 1'
    PRESSURE_2_TEMP = 'Temp pressure 2'


class SensorNames:
    CO2 = 'CO2 sensor'
    HTU = 'HTU21DF-1 sensor'
    DS1 = 'Mouth'
    DS2 = 'Lungs'
    DS3 = 'Canister Top'
    DS4 = 'Canister Bottom'
    PRESSURE1 = 'Pressure 1'
    PRESSURE2 = 'Pressure 2'


class Sensor(BaseModel):
    hardware_input: str = Field('', editable=False, content_type='text')
    group: str = Field('', content_type='text')
    label: str = Field(..., editable=False, content_type='text')
    minimum: float = Field(..., content_type='numeric')
    low_error: float = Field(..., content_type='numeric')
    low_warning: float = Field(..., content_type='numeric')
    high_warning: float = Field(..., content_type='numeric')
    high_error: float = Field(..., content_type='numeric')
    maximum: float = Field(..., content_type='numeric')
    unit_type: str = Field(..., editable=False, content_type='text')
    possible_units: list[str] = Field(..., editable=False, content_type='text', hidden=True)


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
                 unit_type=UnitTypes.PPM,
                 possible_units=[UnitTypes.PPM])

    Temperature = Sensor(label=Labels.TEMP,
                         minimum=10,
                         low_error=20,
                         low_warning=25,
                         high_warning=35,
                         high_error=38,
                         maximum=50,
                         unit_type=UnitTypes.CELSIUS,
                         possible_units=[UnitTypes.CELSIUS, UnitTypes.FAHRENHEIT])

    Humidity = Sensor(label=Labels.HUMIDITY,
                      minimum=0,
                      low_error=10,
                      low_warning=20,
                      high_warning=80,
                      high_error=90,
                      maximum=100,
                      unit_type=UnitTypes.PERCENTAGE,
                      possible_units=[UnitTypes.PERCENTAGE])

    Pressure = Sensor(label=Labels.PRESSURE,
                      minimum=-1,
                      low_error=-0.5,
                      low_warning=-0.45,
                      high_warning=0.45,
                      high_error=0.5,
                      maximum=1,
                      unit_type=UnitTypes.PRESSURE,
                      possible_units=[UnitTypes.PRESSURE])


class Schema:
    SENSOR_SCHEMA = Sensor.schema()['properties']
    HIDDEN_FIELDS = {key for key, field in SENSOR_SCHEMA.items() if field.get('hidden')}
    NUMERIC_FIELDS = {key for key, field in SENSOR_SCHEMA.items() if field.get('content_type') == 'numeric'}

    MONITOR_TYPES = {
        Labels.CO2: GaugeMonitor(180, False, True, max_percent=1000000),
        Labels.TEMP: TemperatureMonitor(90),
        Labels.HUMIDITY: GaugeMonitor(110),
        Labels.PRESSURE: GaugeMonitor(110),
    }


def set_group(sensor, group, input_name):
    current = sensor.copy()
    current.group = group
    current.hardware_input = input_name
    return current


def set_sensors(groups):
    sensors = {}
    for group_name, relevant_sensors in groups.items():
        for input_name, sensor in relevant_sensors.items():
            sensors[input_name] = set_group(sensor, group_name, input_name)
    return sensors


class Settings:
    DEFAULT = {
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
            InputNames.PRESSURE_1: SensorInstance.Pressure,
            InputNames.PRESSURE_1_TEMP: SensorInstance.Temperature,
        },
        SensorNames.PRESSURE2: {
            InputNames.PRESSURE_2: SensorInstance.Pressure,
            InputNames.PRESSURE_2_TEMP: SensorInstance.Temperature,
        }
    }
    SENSORS = set_sensors(DEFAULT)

    DISPLAY = [
        [InputNames.CO2, InputNames.CO2_TEMP, InputNames.CO2_HUMIDITY, InputNames.HTU_TEMP, InputNames.HTU_HUMIDITY],
        [InputNames.DS_TEMP_1, InputNames.DS_TEMP_2, InputNames.DS_TEMP_3, InputNames.DS_TEMP_4, InputNames.PRESSURE_1,
         InputNames.PRESSURE_1_TEMP, InputNames.PRESSURE_2, InputNames.PRESSURE_2_TEMP]
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


def group_sensors():
    groups = {}
    for input_name, sensor in Settings.SENSORS.items():
        groups.setdefault(sensor.group, {})
        groups[sensor.group][input_name] = sensor
    return groups


class SetupConsts:
    DS_INPUT = [InputNames.DS_TEMP_1, InputNames.DS_TEMP_2, InputNames.DS_TEMP_3, InputNames.DS_TEMP_4]
    COMMANDS = {
        SensorNames.DS1: 24, SensorNames.DS2: 25, SensorNames.DS3: 26, SensorNames.DS4: 27
    }

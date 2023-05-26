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
    TACH = 'Tach'
    TACH_2 = 'Tach2'
    TEMP = 'Temp'
    TIMER = 'Time'
    BATTERY = 'Vbat'
    RECORD_STATUS = 'Record'


class SensorNames:
    FIRST_FAN = 'First Fan Speed'
    SECOND_FAN = 'Second Fan Speed'
    TEMP = 'Temperature'
    BATTERY = 'Battery'


class ContentType:
    NUMERIC = 'numeric'
    TEXT = 'text'


class Sensor(BaseModel):
    hardware_input: str = Field('', editable=False, content_type=ContentType.TEXT)
    group: str = Field('', content_type=ContentType.TEXT)
    label: str = Field(..., editable=False, content_type=ContentType.TEXT)
    minimum: float = Field(..., content_type=ContentType.NUMERIC)
    low_error: float = Field(..., content_type=ContentType.NUMERIC)
    low_warning: float = Field(..., content_type=ContentType.NUMERIC)
    high_warning: float = Field(..., content_type=ContentType.NUMERIC)
    high_error: float = Field(..., content_type=ContentType.NUMERIC)
    maximum: float = Field(..., content_type=ContentType.NUMERIC)
    unit_type: str = Field(..., editable=False, content_type=ContentType.TEXT)
    possible_units: list[str] = Field(..., editable=False, content_type=ContentType.TEXT, hidden=True)


class Labels:
    TEMP = 'Temperature'
    FAN = 'Fan'
    BATTERY = 'battery'


class SensorInstance:
    Temperature = Sensor(label=Labels.TEMP,
                         minimum=10,
                         low_error=10,
                         low_warning=10,
                         high_warning=50,
                         high_error=50,
                         maximum=50,
                         unit_type=UnitTypes.CELSIUS,
                         possible_units=[UnitTypes.CELSIUS, UnitTypes.FAHRENHEIT])

    FanSpeed = Sensor(label=Labels.FAN,
                      minimum=0,
                      low_error=0,
                      low_warning=0,
                      high_warning=300,
                      high_error=300,
                      maximum=300,
                      unit_type=UnitTypes.TACHO,
                      possible_units=[UnitTypes.TACHO])

    Battery = Sensor(label=Labels.BATTERY,
                     minimum=0,
                     low_error=0,
                     low_warning=0,
                     high_warning=100,
                     high_error=100,
                     maximum=100,
                     unit_type=UnitTypes.PERCENTAGE,
                     possible_units=[UnitTypes.PERCENTAGE])


class Schema:
    SENSOR_SCHEMA = Sensor.schema()['properties']
    HIDDEN_FIELDS = {key for key, field in SENSOR_SCHEMA.items() if field.get('hidden')}
    NUMERIC_FIELDS = {key for key, field in SENSOR_SCHEMA.items() if field.get('content_type') == ContentType.NUMERIC}

    MONITOR_TYPES = {
        Labels.TEMP: TemperatureMonitor(90),
        Labels.FAN: GaugeMonitor(110),
        Labels.BATTERY: GaugeMonitor(110),
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
        SensorNames.FIRST_FAN: {
            InputNames.TACH: SensorInstance.FanSpeed,
        },
        SensorNames.SECOND_FAN: {
            InputNames.TACH_2: SensorInstance.FanSpeed,
        },
        SensorNames.TEMP: {
            InputNames.TEMP: SensorInstance.Temperature,
        },
        SensorNames.BATTERY: {
            InputNames.BATTERY: SensorInstance.Battery,
        },
    }
    SENSORS = set_sensors(DEFAULT)

    DISPLAY = [
        [InputNames.TACH, InputNames.TACH_2, InputNames.TEMP, InputNames.BATTERY],
    ]

    GRAPHS = {
        'Temperature': [
            InputNames.TEMP,
        ],
        'Fan Speed': [
            InputNames.TACH,
            InputNames.TACH_2,
        ],
        'Battery': [
            InputNames.BATTERY,
        ],
        'Timer': [
            InputNames.TIMER,
        ],
    }


def group_sensors():
    groups = {}
    for input_name, sensor in Settings.SENSORS.items():
        groups.setdefault(sensor.group, {})
        groups[sensor.group][input_name] = sensor
    return groups


class SetupConsts:
    COMMANDS = {}

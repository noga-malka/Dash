import functools

from pydantic import Field, BaseModel


class Sensor(BaseModel):
    label: str = Field(..., editable=False, content_type='text')
    minimum: int = Field(..., content_type='numeric')
    low: int = Field(..., content_type='numeric')
    high: int = Field(..., content_type='numeric')
    maximum: int = Field(..., content_type='numeric')


class Settings:
    CO2 = Sensor(label='CO2', minimum=300, low=500, high=3000, maximum=5000)
    Temperature = Sensor(label='Temperature', minimum=25, low=28, high=32, maximum=35)
    Humidity = Sensor(label='Humidity', minimum=30, low=40, high=70, maximum=80)
    ALL_SENSORS = [CO2, Temperature, Humidity]

    TYPES = {
        CO2.label: ('slider', 120),
        Temperature.label: ('thermometer', 90),
        Humidity.label: ('gauge', 90),
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
        }
    }
    GRAPHS = {
        'Temperature': [
            'CO2 sensor Temp',
            'HTU21DF-1 sensor Temp',
            'HTU21DF-2 sensor Temp',
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

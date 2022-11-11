import functools

from pydantic import Field, BaseModel


class Sensor(BaseModel):
    label: str = Field(...)
    minimum: int = Field(...)
    low: int = Field(...)
    high: int = Field(...)
    maximum: int = Field(...)


class Settings:
    CO2 = Sensor(label='CO2', minimum=300, low=500, high=3000, maximum=5000)
    Temperature = Sensor(label='Temperature', minimum=25, low=28, high=32, maximum=35)
    Humidity = Sensor(label='Humidity', minimum=30, low=40, high=70, maximum=80)

    TYPES = {
        CO2.json(): ('slider', 120),
        Temperature.json(): ('thermometer', 90),
        Humidity.json(): ('gauge', 90),
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
    SENSORS = functools.reduce(lambda x, y: x | y, GROUPS.values(), {})

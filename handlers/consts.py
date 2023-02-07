class InputTypes:
    SENSORS = 'sensors'
    CO2_CONTROLLER = 'CO2 controller'
    ENGINE = 'engine'


class HardwarePackets:
    DATA = 'Data'
    SETUP = 'setup'
    ONE_WIRE = 'OneWire_count'


class Commands:
    HEADER = 'aa55aa'
    SET_CO2 = 21
    SET_FAN = 22
    SETUP_DS1 = 24
    SETUP_DS2 = 25
    SETUP_DS3 = 26
    SETUP_DS4 = 27
    SCAN = 28
    SEARCH_SENSOR = 29
    COMMAND_DEFAULT = {SET_CO2: '400'}


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1

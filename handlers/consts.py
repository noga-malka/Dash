class InputTypes:
    SENSORS = 'sensors'
    CO2_CONTROLLER = 'CO2 controller'
    ENGINE = 'engine'


class HardwarePackets:
    DATA = 'Data'
    SETUP = 'setup'
    ONE_WIRE = 'OneWire_count'
    FILE = 'file'


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

    class CO2Controller:
        OPEN = 'O'
        CLOSE = 'C'
        AUTO = 'A'
        READ = 'R'

    CLASSIFIER = {
        InputTypes.SENSORS: [SET_FAN, SET_CO2, SETUP_DS1, SETUP_DS2, SETUP_DS3, SETUP_DS4, SEARCH_SENSOR, SCAN],
        InputTypes.CO2_CONTROLLER: [CO2Controller.OPEN, CO2Controller.CLOSE, CO2Controller.AUTO, CO2Controller.READ]
    }


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1

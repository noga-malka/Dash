class InputTypes:
    SENSORS = 'sensors'
    CO2_CONTROLLER = 'CO2 controller'
    ENGINE = 'engine'


class HardwarePackets:
    DATA = 'Data'
    SETUP = 'setup'
    ONE_WIRE = 'OneWire_count'
    FILE = 'file'
    DPC = 'DPC'


class Commands:
    HEADER = 'aa55aa'
    SET_DEVICE_ID = 41
    READ_DEVICE_ID = 42
    READ_ELAPSED_TIME = 36
    RESET_COUNTERS = 35
    SET_FAN = 34
    START_RECORD = 38
    STOP_RECORD = 39

    GET_FILE_LIST = 43
    READ_SINGLE_FILE = 40
    DELETE_FILES = 44


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1

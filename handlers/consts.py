class InputTypes:
    SENSORS = 'sensors'
    CO2_CONTROLLER = 'CO2 controller'
    ENGINE = 'engine'


class HardwarePackets:
    DATA = 'Data'
    FILE = 'file'
    RUN_TIME = 'RunTime'
    TOTAL_TIME = 'TotalTime'
    DEVICE_ID = 'DeviceID'
    FILES_LIST = 'FILE'
    PLAYBACK = 'Playback'

    DISPLAY = [RUN_TIME, TOTAL_TIME, DEVICE_ID]


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

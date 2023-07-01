class DataColumns:
    NAMES = ['Time', 'Temp', 'Vbat', 'Fan', 'Tach', 'Tach2']
    INDEXES = list(range(1, len(NAMES) * 2, 2))
    COUNT = len(NAMES)


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
    SOFTWARE_VERSION = 'SV'
    CLOCK = 'RTC'
    FILES_LIST = 'FILE'
    PLAYBACK = 'Playback'
    PLAYBACK_END = 'END\r'

    DISPLAY = [RUN_TIME, TOTAL_TIME, DEVICE_ID, SOFTWARE_VERSION, CLOCK]


class Commands:
    HEADER = 'aa55aa'
    SET_DEVICE_ID = 41
    READ_DEVICE_ID = 42
    READ_ELAPSED_TIME = 36
    RESET_COUNTERS = 35
    SET_FAN = 45
    SOFTWARE_VERSION = 37
    START_RECORD = 38
    STOP_RECORD = 39
    READ_CLOCK = 47
    WRITE_CLOCK = 48

    GET_FILE_LIST = 43
    READ_SINGLE_FILE = 40
    DELETE_FILES = 44
    READ_FAN_SPEED = 46


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1

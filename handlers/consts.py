from handlers.packetBuilders.dpc_builder import DPCPacketBuilder
from handlers.packetBuilders.sensors_builder import SensorsPacketBuilder


class InputTypes:
    SENSORS = 'sensors'
    CO2_CONTROLLER = 'CO2 controller'
    ENGINE = 'engine'

    MAPPING = {
        SENSORS: {
            'header': '',
            'packet_builder': SensorsPacketBuilder(),
        },
        CO2_CONTROLLER: {
            'header': 'DPC\t',
            'packet_builder': DPCPacketBuilder(),
        },
    }


class HardwarePackets:
    DATA = 'Data'
    SETUP = 'setup'
    ONE_WIRE = 'OneWire_count'
    FILE = 'file'
    DPC = 'DPC'


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
        CARRIAGE_RETURN = '\r'
        OPEN = 'V,M,O'
        CLOSE = 'V,M,C'
        AUTO = 'V,M,A'
        READ = 'FV'
        SET_POINT = 'SP'

        MAPPING = {
            'close': CLOSE,
            'open': OPEN,
            'auto': AUTO,
        }

    CLASSIFIER = {
        SET_FAN: InputTypes.SENSORS,
        SET_CO2: InputTypes.SENSORS,
        SETUP_DS1: InputTypes.SENSORS,
        SETUP_DS2: InputTypes.SENSORS,
        SETUP_DS3: InputTypes.SENSORS,
        SETUP_DS4: InputTypes.SENSORS,
        SEARCH_SENSOR: InputTypes.SENSORS,
        SCAN: InputTypes.SENSORS,
        CO2Controller.OPEN: InputTypes.CO2_CONTROLLER,
        CO2Controller.CLOSE: InputTypes.CO2_CONTROLLER,
        CO2Controller.AUTO: InputTypes.CO2_CONTROLLER,
        CO2Controller.READ: InputTypes.CO2_CONTROLLER,
    }


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1

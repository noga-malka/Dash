from handlers.consts import Commands
from handlers.packetBuilders.sensors_builder import SensorsPacketBuilder
from handlers.packetBuilders.text_builder import TextPacketBuilder

MAPPING = {
    Commands.START_RECORD: TextPacketBuilder,
    Commands.READ_SINGLE_FILE: TextPacketBuilder,
    Commands.SET_DEVICE_ID: SensorsPacketBuilder,
    Commands.READ_CLOCK: SensorsPacketBuilder,
    Commands.WRITE_CLOCK: SensorsPacketBuilder,
    Commands.STOP_RECORD: SensorsPacketBuilder,
    Commands.READ_DEVICE_ID: SensorsPacketBuilder,
    Commands.READ_ELAPSED_TIME: SensorsPacketBuilder,
    Commands.RESET_COUNTERS: SensorsPacketBuilder,
    Commands.SET_FAN: SensorsPacketBuilder,
    Commands.SOFTWARE_VERSION: SensorsPacketBuilder,
    Commands.GET_FILE_LIST: SensorsPacketBuilder,
    Commands.DELETE_FILES: SensorsPacketBuilder,
}

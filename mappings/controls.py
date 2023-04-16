from handlers.consts import InputTypes
from handlers.packetBuilders.sensors_builder import SensorsPacketBuilder

CONTROLS = {
    InputTypes.SENSORS: {
        'packet_builder': SensorsPacketBuilder(),
    },
}

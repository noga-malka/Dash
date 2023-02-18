from handlers.consts import InputTypes
from handlers.packetBuilders.dpc_builder import DPCPacketBuilder
from handlers.packetBuilders.sensors_builder import SensorsPacketBuilder
from tabs.control_panel import dpc_controls, sensors_controls

CONTROLS = {
    InputTypes.SENSORS: {
        'header': '',
        'packet_builder': SensorsPacketBuilder(),
        'generator': sensors_controls
    },
    InputTypes.CO2_CONTROLLER: {
        'header': 'DPC\t',
        'packet_builder': DPCPacketBuilder(),
        'generator': dpc_controls
    },
}

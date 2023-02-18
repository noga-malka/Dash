from consts import InputModes, TagIds
from handlers.bluethooth_reader import BluetoothHandler
from handlers.consts import InputTypes
from handlers.file_handler import FileHandler
from handlers.mutliple_serial_handler import MultipleSerialHandler
from tabs.control_panel import dpc_controls, sensors_controls, file_extra, bluetooth_extra, serial_extra
from tabs.graph_monitor import GraphPage
from tabs.live_monitor import LivePage
from tabs.set_config import ConfigPage

CONTROLS = {
    InputTypes.CO2_CONTROLLER: dpc_controls,
    InputTypes.SENSORS: sensors_controls,
}

EXTRA = {
    InputModes.FILE: file_extra(),
    InputModes.BLUETOOTH: bluetooth_extra(),
    InputModes.SERIAL: serial_extra()
}

TYPES = {
    InputModes.SERIAL: MultipleSerialHandler(),
    InputModes.BLUETOOTH: BluetoothHandler(),
    InputModes.FILE: FileHandler()
}

PAGES = {
    'monitor': {'label': 'Monitor Panel', TagIds.Layout.CONTENT: LivePage()},
    'graph': {'label': 'Graph Panel', TagIds.Layout.CONTENT: GraphPage()},
    'config': {'label': 'Configurations', TagIds.Layout.CONTENT: ConfigPage()}
}

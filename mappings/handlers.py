from consts import InputModes
from handlers.bluethooth_reader import BluetoothHandler
from handlers.file_handler import FileHandler
from handlers.mutliple_serial_handler import MultipleSerialHandler
from tabs.control_panel import file_extra, bluetooth_extra, serial_extra

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

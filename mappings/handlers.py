from consts import InputModes
from handlers.bluethooth_reader import BluetoothHandler
from handlers.file_handler import FileHandler
from tabs.control_panel import file_extra, live_stream_extra

EXTRA = {
    InputModes.FILE: file_extra(),
    InputModes.BLUETOOTH: live_stream_extra()
}

TYPES = {
    InputModes.BLUETOOTH: BluetoothHandler(),
    InputModes.FILE: FileHandler()
}

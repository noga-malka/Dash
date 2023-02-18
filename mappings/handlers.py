from consts import InputModes
from handlers.file_handler import FileHandler
from handlers.mutliple_serial_handler import MultipleInputsHandler
from tabs.control_panel import file_extra, serial_extra

EXTRA = {
    InputModes.FILE: file_extra(),
    InputModes.SERIAL: serial_extra()
}

TYPES = {
    InputModes.SERIAL: MultipleInputsHandler(),
    InputModes.FILE: FileHandler()
}

from consts import InputModes
from handlers.file_handler import FileHandler
from handlers.mutliple_serial_handler import MultipleInputsHandler
from tabs.control_panel import file_extra, live_stream_extra

EXTRA = {
    InputModes.FILE: file_extra(),
    InputModes.STREAMING: live_stream_extra()
}

TYPES = {
    InputModes.STREAMING: MultipleInputsHandler(),
    InputModes.FILE: FileHandler()
}

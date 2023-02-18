import pathlib
import sys
from enum import Enum

import dash_bootstrap_components as dbc

IS_DEBUG = len(sys.argv) > 1 and sys.argv[1] == 'debug'


class TagFields:
    IS_OPEN = 'is_open'
    CLICK = 'n_clicks'
    INTERVAL = 'n_intervals'
    VALUE = 'value'
    CLASS_NAME = 'className'
    STYLE = 'style'
    CHILDREN = 'children'
    OPTIONS = 'options'
    DATA = 'data'
    ON = 'on'
    DISABLED = 'disabled'
    MIN = 'min'
    MAX = 'max'
    LABEL = 'label'
    PATH = 'pathname'


class TagIds:
    LOCATION = 'url'
    TABS = 'tabs'
    TEMP_SWITCH = 'temperature_switch'
    PLACEHOLDER = 'placeholder'
    CLOCK = 'timer'
    THEME = 'theme'

    class Layout:
        THEME = 'theme_layout'
        CONTENT = 'content_layout'
        EXTRA = 'extra_layout'

    class Intervals:
        ONE_SECOND = 'interval'
        THREE_SECONDS = 'read_board'
        ONE_MINUTE = 'save_data'

        VALUES = {
            ONE_SECOND: 1000,
            THREE_SECONDS: 3000,
            ONE_MINUTE: 60000,
        }

        @staticmethod
        def create_interval(name: str):
            return dict(id=name, interval=TagIds.Intervals.VALUES[name], n_intervals=0)

    class Modals:
        class Save:
            MODAL = 'save_file'
            DOWNLOAD = 'download_text'
            BUTTON = 'save_session'

        class Clean:
            MODAL = 'are_you_sure'
            YES = 'sure_yes'
            NO = 'sure_no'

        class Bluetooth:
            MODAL = 'bluetooth_modal'
            SCAN = 'scan_bluetooth'
            INPUT = 'mac_input'
            CONNECT = 'mac_button'

        class Serial:
            MODAL = 'serial_modal'
            CONNECTIONS = 'selected_connections'
            SCAN = 'scan_comports'
            ADD = 'add_serial'
            CLEAR = 'clear_serial'
            INPUT = 'serial_input'
            INPUT_TYPE = 'input_type'
            CONNECT = 'serial_connect'

    class Tabs:
        class Config:
            TABLE = 'configuration'
            SAVE_TABLE = 'save_config'
            RESET_TOGGLES = 'reset_toggles'
            SENSOR_STATUS = 'sensor_count'
            SCAN = 'scan_board'
            MODAL = 'config_board'
            OPEN_MODAL = 'open_config_board'

        class Monitors:
            class Control:
                PANEL = 'control_panel'
                TOGGLE_PANEL = 'expand_panel'
                SP_SLIDER = 'sp_slider'
                DPC = 'dpc_mode_selector'
                CO2 = 'set_co2'
                CO2_VALUE = 'co2_value'
                FAN = 'set_fan'
                COMMAND = 'command'
                DATA = 'custom_data'
                SEND = 'send_command'
                ENGINE = 'activate_engine'
                ENGINE_SPEED = 'engine_speed'

            UPLOAD_FILE = 'upload_file'


class Icons:
    class Css:
        DOWN = 'fa fa-angle-down fa-lg'
        UP = 'fa fa-angle-up fa-lg'
        SAVE = 'fa fa-bookmark fa-lg'
        CLEAN = 'fa fa-eraser fa-lg'

        SERIAL = 'fa fa-plug fa-lg icon'
        BLUETOOTH = 'fa fa-wifi fa-lg icon'
        RANDOM = 'fa fa-random fa-lg icon'
        UPLOAD = 'fa fa-upload fa-lg icon'

        CHECK = 'fa fa-check-circle fa-lg'
        WARNING = 'fa fa-exclamation-circle fa-lg'
        ERROR = 'fa fa-times-circle fa-lg'

        MOON = 'fa fa-moon'
        SUN = 'fa fa-sun'

    SAVE = {'id': 'save', 'icon': Css.SAVE}
    CLEAN = {'id': 'clean', 'icon': Css.CLEAN}

    ALL = [SAVE, CLEAN]


class InputModes:
    SERIAL = 'serial'
    BLUETOOTH = 'bluetooth'
    FILE = 'file'
    ALL = {
        SERIAL: {'icon': Icons.Css.SERIAL, 'label': 'Serial'},
        BLUETOOTH: {'icon': Icons.Css.BLUETOOTH, 'label': 'Bluetooth'},
        FILE: {'icon': Icons.Css.UPLOAD, 'label': 'From File'},
    }


class DatabaseReader(Enum):
    FIRST = 0
    LAST = -1
    ALL = 'all'


class DatabaseTypes:
    ROW = 'row'
    SINGLE_VALUE = 'single'
    DATAFRAME = 'dataframe'


class DaqConsts:
    GRADIENT = {"gradient": True, "ranges": {"red": [0, 20], "yellow": [20, 50], "green": [50, 100]}}
    ICONS = {"right": Icons.Css.MOON, "left": Icons.Css.SUN}


class Colors(Enum):
    GOOD = '#69c569'
    WARNING = 'orange'
    ERROR = '#ff4900'
    DISCONNECTED = 'red'


class Theme:
    DAQ_THEME = {
        'dark': False,
        'detail': '#8F8DF5',
        'primary': '#349FFC',
        'secondary': '#C0D0E2',
    }
    FIGURE_LIGHT = 'cerulean'
    FIGURE_DARK = 'darkly'
    DARK = dbc.themes.DARKLY
    LIGHT = dbc.themes.CERULEAN


class ValueRange:
    LEVEL_COMPARE = {
        ('minimum', 'low_error'): Colors.ERROR,
        ('low_error', 'low_warning'): Colors.WARNING,
        ('low_warning', 'high_warning'): Colors.GOOD,
        ('high_warning', 'high_error'): Colors.WARNING,
        ('high_error', 'maximum'): Colors.ERROR,
    }
    ICONS = {
        Colors.GOOD: Icons.Css.CHECK,
        Colors.WARNING: Icons.Css.WARNING,
        Colors.ERROR: Icons.Css.WARNING,
        Colors.DISCONNECTED: Icons.Css.ERROR,
    }


def to_celsius(value):
    return int((value - 32) * 5 / 9)


def to_fahrenheit(value):
    return int(value * 1.8 + 32)


class UnitTypes:
    CELSIUS = 'C°'
    FAHRENHEIT = 'F°'
    PPM = 'PPM'
    PERCENTAGE = '%'
    PRESSURE = 'BAR'
    SET_POINT = 'SP'
    CONVERT = {
        FAHRENHEIT: to_fahrenheit
    }
    CANCEL = {
        FAHRENHEIT: to_celsius
    }

    @staticmethod
    def get_converter(unit_type: str, cancel=False):
        if cancel:
            return UnitTypes.CANCEL.get(unit_type, lambda value: value)
        return UnitTypes.CONVERT.get(unit_type, lambda value: value)


class NavButtons:
    DEFAULT = 'default'
    CLICKED = 'clicked'
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
    OPTIONS = {
        DEFAULT: {'color': 'inherit', 'message': ''},
        CLICKED: {'color': 'var(--bs-primary)', 'message': ''},
        CONNECTED: {'color': 'var(--bs-success)', 'message': 'Connected: {current}'},
        DISCONNECTED: {'color': 'var(--bs-warning)', 'message': 'Failed to Connect: {current}'},
    }


class OutputDirectory:
    ROOT = pathlib.Path('output')
    TEMP_FILE = ROOT / 'temporary.csv'
    CONFIG_FILE = ROOT / 'configuration.json'

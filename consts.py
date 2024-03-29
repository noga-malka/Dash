import pathlib
import sys
from enum import Enum

import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

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
        SYNC_DATA = 'interval'
        COUNT_SENSORS = 'read_board'
        SAVE_TEMPORARY_FILE = 'save_data'

        VALUES = {
            SYNC_DATA: 1000,
            COUNT_SENSORS: 5000,
            SAVE_TEMPORARY_FILE: 60000,
        }

        @staticmethod
        def create_interval(name: str):
            return dict(id=name, interval=TagIds.Intervals.VALUES[name], n_intervals=0)

    class Buttons:
        RECORDING = 'recording'
        SAVE = 'save_button'
        CLEAN = 'clean_button'

    class Modals:
        class Save:
            MODAL = 'save_file'
            DOWNLOAD = 'download_text'
            BUTTON = 'save_session'

        class Clean:
            MODAL = 'are_you_sure'
            YES = 'sure_yes'
            NO = 'sure_no'

        class LiveStream:
            MODAL = 'live_modal'
            CONNECTIONS = 'selected_connections'
            SCAN = 'scan_connections'
            ADD = 'add_connection'
            CLEAR = 'clear_connections'
            INPUT = 'input_stream'
            INPUT_TYPE = 'input_type'
            CONNECT = 'stream_connect'

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
                BREATH_DEPTH = 'breath_depth'
                BREATH_RATE = 'breath_rate'

            UPLOAD_FILE = 'upload_file'


class Icons:
    class Css:
        DOWN = DashIconify(icon='material-symbols:keyboard-double-arrow-down-rounded', width=30)
        UP = DashIconify(icon='material-symbols:keyboard-double-arrow-up-rounded', width=30)
        SAVE = DashIconify(icon='material-symbols:save', width=30)
        CLEAN = DashIconify(icon='majesticons:eraser', width=30)
        TIMER = DashIconify(icon='material-symbols:timer-rounded', width=30)
        START_RECORD = DashIconify(icon='material-symbols:play-circle-rounded', width=30)
        STOP_RECORD = DashIconify(icon='ic:round-stop-circle', width=30)

        LIVE_STREAM = DashIconify(icon='material-symbols:monitor-heart-outline-rounded', width=30)
        UPLOAD = DashIconify(icon='material-symbols:upload-file-rounded', width=30)

        CELSIUS = DashIconify(icon='carbon:temperature-celsius', width=30)
        FAHRENHEIT = DashIconify(icon='carbon:temperature-fahrenheit', width=30)

        CHECK = 'fa fa-check-circle fa-lg'
        WARNING = 'fa fa-exclamation-circle fa-lg'
        ERROR = 'fa fa-times-circle fa-lg'

        MOON = 'fa fa-moon'
        SUN = 'fa fa-sun'

    SAVE = dict(id=TagIds.Buttons.SAVE, label='Save', icon=Css.SAVE)
    CLEAN = dict(id=TagIds.Buttons.CLEAN, label='Reset', icon=Css.CLEAN)
    START_RECORD = dict(id=TagIds.Buttons.RECORDING, label='Start Recording', icon=Css.START_RECORD)
    STOP_RECORD = dict(id=TagIds.Buttons.RECORDING, label='Stop Recording', icon=Css.STOP_RECORD)
    TIMER = dict(id=TagIds.CLOCK, label='Timer', icon=Css.TIMER)
    ALL = [TIMER, SAVE, CLEAN, START_RECORD]


class InputModes:
    STREAMING = 'streaming'
    FILE = 'file'
    ALL = {
        STREAMING: {'icon': Icons.Css.LIVE_STREAM, 'label': 'Live Stream'},
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


class GraphConsts:
    MAX_ROWS = 10000


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

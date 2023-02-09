import pathlib
import sys
from enum import Enum

import dash_bootstrap_components as dbc

IS_DEBUG = len(sys.argv) > 1 and sys.argv[1] == 'debug'


class TagIds:
    RANGE = 'range'
    CHECKLIST = 'checklist'
    TABS = 'tabs'
    INTERVAL = 'interval'
    GRAPH = 'graph'
    CO2_BUTTON = 'set_co2'
    FAN_BUTTON = 'set_fan'


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

    SERIAL = {'id': 'serial', 'icon': Css.SERIAL}
    BLUETOOTH = {'id': 'bluetooth', 'icon': Css.BLUETOOTH}
    RANDOM = {'id': 'random', 'icon': Css.RANDOM}
    UPLOAD = {'id': 'upload', 'icon': Css.UPLOAD}

    ALL = [SAVE, CLEAN]
    INPUT_MODES = [{'icon': SERIAL, 'label': 'Serial'},
                   {'icon': BLUETOOTH, 'label': 'Bluetooth'},
                   {'icon': UPLOAD, 'label': 'Load File'}]
    if IS_DEBUG:
        INPUT_MODES.append({'icon': RANDOM, 'label': 'Random Data'})


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
        PRESSURE: lambda value: value,
        PERCENTAGE: lambda value: value,
        PPM: lambda value: value,
        CELSIUS: lambda value: value,
        SET_POINT: lambda value: value,
        FAHRENHEIT: to_fahrenheit
    }
    CANCEL = {
        PRESSURE: lambda value: value,
        PERCENTAGE: lambda value: value,
        PPM: lambda value: value,
        CELSIUS: lambda value: value,
        SET_POINT: lambda value: value,
        FAHRENHEIT: to_celsius
    }


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

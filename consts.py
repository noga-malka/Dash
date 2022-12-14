import sys
from enum import Enum

import dash_bootstrap_components as dbc

IS_DEBUG = len(sys.argv) > 1 and sys.argv[1] == 'debug'


class RealtimeConsts:
    GAP = 210
    STEP = 1


class TagIds:
    RANGE = 'range'
    CHECKLIST = 'checklist'
    TABS = 'tabs'
    INTERVAL = 'interval'
    GRAPH = 'graph'
    CO2_BUTTON = 'set_co2'
    FAN_BUTTON = 'set_fan'

    class Icons:
        BACKWARD = {'id': 'backward', 'icon': 'fa-fast-backward'}
        START = {'id': 'to-start', 'icon': 'fa-step-backward'}
        PLAY = {'id': 'play', 'icon': 'fa-play'}
        PAUSE = {'id': 'pause', 'icon': 'fa-pause-circle'}
        SAVE = {'id': 'save', 'icon': 'fa-bookmark'}
        CLEAN = {'id': 'clean', 'icon': 'fa-eraser'}
        FORWARD = {'id': 'forward', 'icon': 'fa-fast-forward'}
        END = {'id': 'to-end', 'icon': 'fa-step-forward'}
        SERIAL = {'id': 'serial', 'icon': 'fa-plug'}
        BLUETOOTH = {'id': 'bluetooth', 'icon': 'fa-wifi'}
        RANDOM = {'id': 'random', 'icon': 'fa-random'}
        UPLOAD = {'id': 'upload', 'icon': 'fa-upload'}
        WARNING = 'fa-exclamation-circle'
        CHECK = 'fa-check-circle'

        ALL = [SAVE, PLAY, PAUSE, CLEAN]
        INPUT_MODES = [{'icon': SERIAL, 'label': 'Serial'},
                       {'icon': BLUETOOTH, 'label': 'Bluetooth'},
                       {'icon': UPLOAD, 'label': 'Load File'}]
        if IS_DEBUG:
            INPUT_MODES.append({'icon': RANDOM, 'label': 'Random Data'})


class Commands:
    HEADER = 'aa55aa'
    SET_CO2 = 15
    SET_FAN = 16
    COMMAND_DEFAULT = {SET_CO2: '400'}
    ALL = [SET_CO2]


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1


class DaqConsts:
    GRADIENT = {"gradient": True, "ranges": {"red": [0, 20], "yellow": [20, 50], "green": [50, 100]}}
    ICONS = {"right": "fa fa-moon", "left": "fa fa-sun"}


class Colors(Enum):
    GOOD = '#69c569'
    WARNING = 'orange'
    ERROR = 'red'


class Theme:
    DAQ_THEME = {
        'dark': True,
        'detail': '#8F8DF5',
        'primary': '#349FFC',
        'secondary': '#C0D0E2',
    }
    FIGURE_LIGHT = 'CERULEAN'
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


def to_celsius(value):
    return int((value - 32) * 5 / 9)


def to_fahrenheit(value):
    return int(value * 1.8 + 32)


class UnitTypes:
    CELSIUS = 'C°'
    FAHRENHEIT = 'F°'
    PPM = 'PPM'
    PERCENTAGE = '%'
    CONVERT = {
        PERCENTAGE: lambda value: value,
        PPM: lambda value: value,
        CELSIUS: lambda value: value,
        FAHRENHEIT: to_fahrenheit
    }
    CANCEL = {
        PERCENTAGE: lambda value: value,
        PPM: lambda value: value,
        CELSIUS: lambda value: value,
        FAHRENHEIT: to_celsius
    }

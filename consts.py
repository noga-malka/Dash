import dash_bootstrap_components as dbc


class RealtimeConsts:
    GAP = 210
    STEP = 4


class TagIds:
    RANGE = 'range'
    CHECKLIST = 'checklist'
    TABS = 'tabs'
    INTERVAL = 'interval'
    GRAPH = 'graph'

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

        ALL = [START, BACKWARD, PLAY, PAUSE, SAVE, CLEAN, FORWARD, END]
        INPUT_MODES = [{'icon': SERIAL, 'label': 'Serial'},
                       {'icon': BLUETOOTH, 'label': 'Bluetooth'},
                       {'icon': RANDOM, 'label': 'Random Data'},
                       {'icon': UPLOAD, 'label': 'Load File'}]


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1


class Bluetooth:
    DEFAULT_ADDRESS = 'B8:D6:1A:A7:43:32'


class DaqConsts:
    GRADIENT = {"gradient": True, "ranges": {"red": [0, 20], "yellow": [20, 50], "green": [50, 100]}}
    ICONS = {"right": "fa fa-moon", "left": "fa fa-sun"}


class Theme:
    FIGURE_LIGHT = 'lumen'
    FIGURE_DARK = 'darkly'
    DARK = dbc.themes.DARKLY
    LIGHT = dbc.themes.LUMEN

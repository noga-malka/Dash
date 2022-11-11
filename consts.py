class GraphConsts:
    FIGURES = [
        ['CO2 sensor Temp', 'HTU21DF-1 sensor Temp', 'HTU21DF-2 sensor Temp'],
        ['CO2 sensor Hum', 'HTU21DF-1 sensor Humidity', 'HTU21DF-2 sensor Humidity'],
        ['CO2 sensor CO2'],
    ]
    ALL = sum(FIGURES, [])


class DashConsts:
    CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"


class TagIds:
    RANGE = 'range'
    CHECKLIST = 'checklist'
    TABS = 'tabs'
    INTERVAL = 'interval'
    GRAPH = 'graph'

    class Icons:
        START = {'id': 'to-start', 'icon': 'fa-fast-backward'}
        PLAY = {'id': 'play', 'icon': 'fa-play'}
        PAUSE = {'id': 'pause', 'icon': 'fa-pause-circle'}
        SAVE = {'id': 'save', 'icon': 'fa-bookmark'}
        CLEAN = {'id': 'clean', 'icon': 'fa-eraser'}
        END = {'id': 'to-end', 'icon': 'fa-fast-forward'}

        ALL = [START, PLAY, PAUSE, SAVE, CLEAN, END]


class DataConsts:
    SENSOR = 'sensor'
    TIME = 'time'
    VALUE = 'value'


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1


class Bluetooth:
    DEFAULT_ADDRESS = 'B8:D6:1A:A7:43:32'


class DaqConsts:
    GRADIENT = {"gradient": True, "ranges": {"red": [0, 20], "yellow": [20, 50], "green": [50, 100]}}
    ICONS = {"right": "fa fa-moon", "left": "fa fa-sun"}

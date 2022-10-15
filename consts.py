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


class DataConsts:
    SENSOR = 'sensor'
    TIME = 'time'
    VALUE = 'value'


class Uart:
    BAUDRATE = 115200
    TIMEOUT = 1


class Bluetooth:
    DEFAULT_ADDRESS = 'B8:D6:1A:A7:43:32'

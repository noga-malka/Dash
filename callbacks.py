import base64
from io import StringIO

import dash_bootstrap_components as dbc
import pandas
from dash import Dash, Input, Output, callback_context, ALL
from dash.exceptions import PreventUpdate

from configurations import Settings
from consts import TagIds
from layout import generate_layout
from realtime_data import realtime
from stoppable_thread import StoppableThread
from tabs.file_monitor import FilePage
from tabs.live_monitor import LivePage
from utilities import generate_color, generate_sensor_output, activate_live

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO], suppress_callback_exceptions=True)
app.layout = generate_layout()

pages = {
    'live': LivePage(),
    'file': FilePage(),
}
thread = None


@app.callback(Output('page', 'children'),
              Input(TagIds.TABS, 'value'))
def render_content(tab):
    global thread
    if tab == 'live' and not thread:
        thread = StoppableThread(target=activate_live, daemon=True, cleanup=lambda: realtime.clean())
        thread.start()
    elif tab != 'live' and thread:
        thread = thread.stop()
    return pages[tab].render()


@app.callback(*sum([generate_sensor_output(sensor) for sensor in Settings.SENSORS], []),
              *[Output(group + '_time', 'children') for group in Settings.GROUPS],
              Input(TagIds.INTERVAL, 'n_intervals'),
              Input(TagIds.TABS, 'value'), prevent_initial_call=True)
def update_sensors(n_intervals, tab):
    if callback_context.triggered_id == TagIds.TABS:
        raise PreventUpdate
    timestamp = None
    if len(realtime.graph) == 0:
        content = {name: sensor.minimum for name, sensor in Settings.SENSORS.items()}
    else:
        try:
            content = realtime.read_data()
            start = pandas.Timestamp(realtime.graph.iloc[0].name).strftime('%Y-%m-%d %H:%M:%S')
            end = pandas.Timestamp(content.name).strftime('%Y-%m-%d %H:%M:%S')
            timestamp = start + " - " + end
        except IndexError:
            raise PreventUpdate
    timestamp = [timestamp] * len(Settings.GROUPS)
    return sum([generate_color(content[name], sensor) for name, sensor in Settings.SENSORS.items()], []) + timestamp


@app.callback(Output({'type': 'icon', 'index': ALL}, 'style'),
              Input({'type': 'icon', 'index': ALL}, 'n_clicks'), prevent_initial_call=True)
def render_content(button):
    clicked = callback_context.triggered_id['index']
    colors = [None if clicked != icon['id'] else 'red' for icon in TagIds.Icons.ALL]
    realtime.config[clicked]()
    return [{'color': value} for value in colors]


@app.callback(Output('placeholder', 'children'),
              Input('upload-file', 'contents'), prevent_initial_call=True)
def render_content(content):
    if content:
        data = content.encode("utf8").split(b";base64,")[1]
        data = StringIO(base64.decodebytes(data).decode('utf8'))
        realtime.load_data(pandas.read_csv(data, index_col='time'))
    return {}

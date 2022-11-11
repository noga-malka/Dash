import base64
from io import StringIO

import pandas
import plotly.express as px
from dash import Dash, Input, Output, callback_context, ALL, dcc, html
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from configurations import Settings
from consts import TagIds, Theme
from layout import generate_layout
from realtime_data import realtime
from stoppable_thread import StoppableThread
from tabs.graph_monitor import GraphPage
from tabs.live_monitor import LivePage
from utilities import generate_color, generate_sensor_output, activate_live, parse_time

app = Dash(__name__, external_stylesheets=[Theme.DARK], suppress_callback_exceptions=True)
app.layout = generate_layout()

pages = {
    'monitor': LivePage(),
    'graph': GraphPage()
}
thread = None
last_handler = None


@app.callback(Output('page', 'children'), Input(TagIds.TABS, 'value'))
def render_content(tab):
    return html.Div(id='extra'), *pages[tab].render()


@app.callback(Output('extra', 'children'), Input('url', 'pathname'))
def activate_reader_thread(path: str):
    global thread
    global last_handler
    path = path.strip('/')
    if last_handler == path:
        raise PreventUpdate
    last_handler = path
    if thread:
        thread.stop()
    if path != TagIds.Icons.UPLOAD['id']:
        thread = StoppableThread(target=activate_live, args=(path,), daemon=True, cleanup=lambda: realtime.clean())
        thread.start()
    else:
        return dcc.Upload(id='upload-file', children=html.Div(['Drag and Drop'])),


@app.callback(*sum([generate_sensor_output(sensor) for sensor in Settings.SENSORS], []),
              *[Output(group + '_time', 'children') for group in Settings.GROUPS],
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def update_sensors(n_intervals):
    timestamp = None
    if len(realtime.graph) == 0:
        content = {name: sensor.minimum for name, sensor in Settings.SENSORS.items()}
    else:
        try:
            content = realtime.read_data()
            timestamp = parse_time(realtime.graph.iloc[0].name) + " - " + parse_time(content.name)
        except IndexError:
            raise PreventUpdate
    timestamp = [timestamp] * len(Settings.GROUPS)
    return sum([generate_color(content[name], sensor) for name, sensor in Settings.SENSORS.items()], []) + timestamp


@app.callback(Output({'type': 'icon', 'index': ALL}, 'style'),
              Input({'type': 'icon', 'index': ALL}, 'n_clicks'), prevent_initial_call=True)
def click_navigation_bar_buttons(button):
    clicked = callback_context.triggered_id['index']
    colors = [None if clicked != icon['id'] else 'red' for icon in TagIds.Icons.ALL]
    realtime.config[clicked]()
    return [{'color': value} for value in colors]


@app.callback(Output('placeholder', 'children'), Input('upload-file', 'contents'), prevent_initial_call=True)
def load_file_data(content):
    if content:
        data = content.encode("utf8").split(b";base64,")[1]
        data = StringIO(base64.decodebytes(data).decode('utf8'))
        realtime.load_data(pandas.read_csv(data, index_col='time'))


@app.callback(*[Output(name + '_graph', 'figure') for name in Settings.GRAPHS],
              Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def create_graphs(toggle, interval):
    if realtime.is_paused:
        raise PreventUpdate
    figures = []
    for name, sensors in Settings.GRAPHS.items():
        content = realtime.graph[list(set(realtime.graph.columns).intersection(set(sensors)))]
        graph = px.line(content, title=name)
        if len(content) > 0:
            graph.update_layout({'yaxis': {'range': [min(content.min()), max(content.max())]},
                                 'xaxis': {'range': [min(content.index), max(content.index)]}},
                                template=Theme.FIGURE_DARK if toggle else Theme.FIGURE_LIGHT)
        figures.append(graph)
    return figures

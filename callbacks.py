import plotly.express as px
from dash import Dash, Input, Output, callback_context, ALL, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from configurations import Settings
from consts import TagIds, Theme
from layout import generate_layout, pages
from realtime_data import realtime
from stoppable_thread import types
from tabs.extras import EXTRA
from utilities import generate_color, generate_sensor_output, parse_time

app = Dash(__name__, external_stylesheets=[Theme.DARK], suppress_callback_exceptions=True)
app.layout = generate_layout()


@app.callback(Output('page', 'children'), Input(TagIds.TABS, 'value'), Input('url', 'pathname'))
def render_content(tab, url):
    return *EXTRA.get(url.strip('/'), []), *pages[tab]['page'].render()


@app.callback(Output('placeholder', 'className'), Input('url', 'pathname'))
def activate_reader_thread(path: str):
    path = path.strip('/')
    if realtime.thread.handler_name == path:
        raise PreventUpdate
    realtime.thread.set_handler(path)
    realtime.thread.connect_handler()


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
            timestamp = 'timer: ' + parse_time(content.name, realtime.graph.iloc[0].name)
        except IndexError:
            raise PreventUpdate
    timestamp = [timestamp] * len(Settings.GROUPS)
    return sum([generate_color(content[name], sensor) for name, sensor in Settings.SENSORS.items()], []) + timestamp


@app.callback(Output({'type': 'icon', 'index': ALL}, 'style'),
              Input({'type': 'icon', 'index': ALL}, 'n_clicks'), prevent_initial_call=True)
def click_navigation_bar_buttons(button):
    clicked = callback_context.triggered_id['index']
    colors = [None if clicked != icon['id'] else 'red' for icon in TagIds.Icons.ALL]
    realtime.config.get(clicked, lambda: None)()
    return [{'color': value} for value in colors]


@app.callback(
    Output("modal", "is_open"),
    Input({'type': 'icon', 'index': 'terminal'}, 'n_clicks'),
    [State("modal", "is_open")],
)
def toggle_modal(click, is_open):
    if click:
        return not is_open
    return is_open


@app.callback(
    Output("bluetooth_modal", "is_open"),
    Input('toggle_bluetooth', 'n_clicks'),
    [State("bluetooth_modal", "is_open")],
)
def toggle_modal(click, is_open):
    if click:
        return not is_open
    return is_open


@app.callback(
    Output("toggle_bluetooth", "children"),
    Input('mac_button', 'n_clicks'),
    [State("mac_input", "value")], prevent_initial_call=True
)
def toggle_modal(click, mac_address):
    button_text = 'Failed to connect. Try again'
    if mac_address:
        realtime.thread.connect_handler(address=mac_address)
        if realtime.thread.events.Finish.connect.is_set():
            button_text = 'Connected to: ' + mac_address
    return button_text


@app.callback(Output('placeholder', 'children'), Input('upload-file', 'contents'), prevent_initial_call=True)
def load_file_data(content):
    if content:
        realtime.thread.connect_handler(content=content)


@app.callback(*[Output(name + '_graph', 'figure') for name in Settings.GRAPHS],
              Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def create_graphs(toggle, interval):
    if realtime.is_paused:
        raise PreventUpdate
    figures = []
    for name, sensors in Settings.GRAPHS.items():
        content = realtime.graph[list(set(realtime.graph.columns).intersection(set(sensors)))]
        graph = px.line(content, title=name, template=Theme.FIGURE_DARK if toggle else Theme.FIGURE_LIGHT)
        figures.append(graph)
    return figures


@app.callback(Output('placeholder', 'n_clicks'), State('configuration', 'data'), Input('save_config', 'n_clicks'),
              prevent_initial_call=True)
def load_file_data(config, click):
    config = {row['label']: row for row in config}
    for sensor in Settings.ALL_SENSORS:
        sensor.__dict__.update(config[sensor.label])


@app.callback(Output('placeholder', 'title'), State('command_input', 'value'), State('command_menu', 'value'),
              Input('send_command', 'n_clicks'))
def send_command(content, command, click):
    if click and command:
        types[realtime.thread.handler_name].send_command(command, content)

from datetime import datetime

import dash
import plotly.express as px
from dash import Dash, Input, Output, callback_context, ALL, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from configurations import Settings, Schema
from consts import TagIds, Theme, UnitTypes, Commands
from layout import generate_layout, pages
from realtime_data import realtime
from stoppable_thread import types
from tabs.extras import EXTRA
from tabs.set_config import load_data
from utilities import parse_time, generate_sensors_output

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


@app.callback(generate_sensors_output(),
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def update_sensors(n_intervals):
    if len(realtime.graph) == 0:
        content = {name: sensor.minimum for name, sensor in Settings.SENSORS.items()}
    else:
        try:
            content = realtime.read_data()
        except IndexError:
            raise PreventUpdate
    outputs = [Schema.MONITOR_TYPES[sensor.label].generate_output_values(content[name]) for name, sensor in
               Settings.SENSORS.items()]
    return outputs


@app.callback(Output('timer', 'children'),
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def update_sensors(n_intervals):
    timestamp = 'Timer: '
    try:
        timestamp += parse_time(realtime.graph.iloc[-1].name, realtime.graph.iloc[0].name)
    except IndexError:
        raise PreventUpdate
    return timestamp


@app.callback(Output({'type': 'icon', 'index': ALL}, 'style'),
              Input({'type': 'icon', 'index': ALL}, 'n_clicks'), prevent_initial_call=True)
def click_navigation_bar_buttons(button):
    clicked = callback_context.triggered_id['index']
    colors = [None if clicked != icon['id'] else 'red' for icon in TagIds.Icons.ALL]
    realtime.config.get(clicked, lambda: None)()
    return [{'color': value} for value in colors]


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
    Output("save_file", "is_open"),
    Input({'type': 'icon', 'index': 'save'}, 'n_clicks'),
    [State("save_file", "is_open")],
)
def toggle_modal(click, is_open):
    if click:
        return not is_open
    return is_open


@app.callback(
    Output("are_you_sure", "is_open"),
    Input({'type': 'icon', 'index': 'clean'}, 'n_clicks'),
    Input('sure_no', 'n_clicks'), Input('sure_yes', 'n_clicks'),
    [State("are_you_sure", "is_open")], prevent_initial_call=True
)
def toggle_modal(clicked, no, yes, is_open):
    if callback_context.triggered_id == 'sure_yes':
        realtime.clean()
    return not is_open


@app.callback(
    Output("download_text", "data"),
    Input('save_session', 'n_clicks'))
def toggle_modal(click):
    creation_time = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    return dict(filename=f'output_{creation_time}.csv', content=realtime.graph.to_csv())


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
    if not click:
        raise PreventUpdate
    config = {row['label']: row for row in config}
    for sensor in Schema.ALL:
        current_values = config[sensor.label]
        updates = {key: UnitTypes.CANCEL[sensor.unit_type](value) for key, value in current_values.items() if
                   type(value) == int}
        sensor.__dict__.update(updates)


@app.callback(Output('configuration', 'data'), Input('temperature_switch', 'on'))
def load_file_data(is_celsius):
    unit_type = UnitTypes.CELSIUS if is_celsius else UnitTypes.FAHRENHEIT
    for sensor in Schema.ALL:
        if unit_type in sensor.possible_units:
            sensor.unit_type = unit_type
    return load_data()


@app.callback([[Output(sensor_key, 'min'), Output(sensor_key, 'max'), Output(sensor_key, 'units'),
                Output(sensor_key + '_led', 'label')] for sensor_key in Settings.SENSORS],
              Input('temperature_switch', 'on'))
def change_unit_type(is_celsius):
    unit_type = UnitTypes.CELSIUS if is_celsius else UnitTypes.FAHRENHEIT
    change_function = UnitTypes.CONVERT[unit_type]
    outputs = []
    for name, sensor in Settings.SENSORS.items():
        changes = [dash.no_update] * 4
        if unit_type in sensor.possible_units and sensor.unit_type != unit_type:
            changes = [change_function(sensor.minimum), change_function(sensor.maximum), unit_type, unit_type]
        outputs.append(changes)
    for sensor in Schema.ALL:
        if unit_type in sensor.possible_units:
            sensor.unit_type = unit_type
    return outputs


@app.callback(Output('placeholder', 'title'), Input(TagIds.CO2_BUTTON, 'n_clicks'),
              Input(TagIds.FAN_BUTTON, 'value'), prevent_initial_call=True)
def send_command(co2_click, fan_value):
    if not co2_click and not fan_value:
        raise PreventUpdate
    command = None
    value = None
    if callback_context.triggered_id == TagIds.CO2_BUTTON:
        command, value = Commands.SET_CO2, Commands.COMMAND_DEFAULT[Commands.SET_CO2]
    if callback_context.triggered_id == TagIds.FAN_BUTTON:
        command, value = Commands.SET_FAN, fan_value
    types[realtime.thread.handler_name].send_command(str(command), str(value))

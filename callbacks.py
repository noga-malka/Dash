import os.path
from datetime import datetime

import bluetooth
import dash
import dash_daq as daq
import numpy
import plotly.express as px
from dash import Dash, Input, Output, callback_context, ALL, State, html
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from configurations import Settings, Schema, SetupConsts
from consts import TagIds, Theme, UnitTypes, Commands, Colors, NavButtons, StatusIcons, HardwarePackets
from layout import generate_layout, pages
from realtime_data import realtime
from stoppable_thread import types
from tabs.extras import EXTRA
from tabs.set_config import load_data
from utilities import parse_time, generate_sensors_output

app = Dash(__name__, external_stylesheets=[Theme.DARK], suppress_callback_exceptions=True, title='Caeli')
app.layout = generate_layout()


@app.callback(Output('extra', 'children'), Input('url', 'pathname'))
def render_content(url):
    return EXTRA.get(url.strip('/'), [])


@app.callback(Output('page', 'children'), Input(TagIds.TABS, 'value'))
def render_content(tab):
    return pages[tab]['page'].render()


@app.callback(Output('placeholder', 'className'), Input('url', 'pathname'))
def activate_reader_thread(path: str):
    path = path.strip('/')
    if realtime.thread.handler_name == path:
        raise PreventUpdate
    if realtime.thread.set_handler(path):
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
    outputs = [Schema.MONITOR_TYPES[sensor.label].generate_output_values(sensor, content.get(name, numpy.NaN)) for
               name, sensor in Settings.SENSORS.items()]
    return outputs


@app.callback(Output('mac_input', 'options'), Input('scan_bluetooth', 'n_clicks'))
def scan_bluetooth(clicked):
    devices = {name: mac for (mac, name) in bluetooth.discover_devices(lookup_names=True)}
    types[realtime.thread.handler_name].devices = devices
    return list(devices.keys())


@app.callback(Output('placeholder', 'n_clicks_timestamp'), [Input(group, 'columns') for group in Settings.GROUPS])
def scan_bluetooth(*titles):
    pages['monitor']['page'].saved_names = {title[0]['id']: title[0]['name'] for title in titles}


@app.callback([Output(group + 'header', 'style') for group in Settings.GROUPS], Input(TagIds.INTERVAL, 'n_intervals'))
def scan_bluetooth(clicked):
    try:
        content = realtime.read_data()
    except IndexError:
        raise PreventUpdate
    disconnected = {sensor for sensor in Settings.SENSORS if numpy.isnan(content.get(sensor, numpy.NaN))}
    output = []
    for group_name, sensors in Settings.GROUPS.items():
        color = 'var(--bs-primary)'
        if disconnected.intersection(sensors):
            color = Colors.DISCONNECTED.value
        output.append({'background-color': color})
    return output


@app.callback(Output('timer', 'children'),
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def update_sensors(n_intervals):
    timestamp = 'Timer: '
    if len(realtime.graph):
        timestamp += parse_time(realtime.graph.iloc[-1].name, realtime.graph.iloc[0].name)
    return timestamp


@app.callback(Output({'type': 'icon', 'index': ALL}, 'style'),
              Input({'type': 'icon', 'index': ALL}, 'n_clicks'), prevent_initial_call=True)
def click_navigation_bar_buttons(button):
    clicked = callback_context.triggered_id['index']
    colors = [None if clicked != icon['id'] else 'red' for icon in TagIds.Icons.ALL]
    return [{'color': value} for value in colors]


@app.callback(
    [Output(f'check_{sensor.name}_icon', 'className') for sensor in SetupConsts.DS_TEMP],
    [Output(f'check_{sensor.name}_address', 'children') for sensor in SetupConsts.DS_TEMP],
    [Output(f'check_{sensor.name}', 'on') for sensor in SetupConsts.DS_TEMP],
    Input('reset_toggles', 'n_clicks'),
    [Input(f'check_{sensor.name}', 'on') for sensor in SetupConsts.DS_TEMP],
    prevent_initial_call=True)
def toggle_modal(reset_toggles, *args):
    trigger = callback_context.triggered_id
    empty = [''] * len(SetupConsts.DS_TEMP)
    no_update = [dash.no_update] * len(SetupConsts.DS_TEMP)
    if trigger == 'reset_toggles':
        return *empty, *empty, *[False] * len(SetupConsts.DS_TEMP)
    icons = no_update.copy()
    addresses = no_update.copy()
    for index, sensor in enumerate(SetupConsts.DS_TEMP):
        if trigger == f'check_{sensor.name}':
            if not args[index]:
                icons[index] = ''
                addresses[index] = ''
            else:
                success = realtime.send_command(realtime.thread.events.set_device, SetupConsts.COMMANDS[sensor.name], 0)
                addresses[index] = realtime.command_outputs[HardwarePackets.SETUP] if success else dash.no_update
                icons[index] = f'fa {StatusIcons.CHECK if success else StatusIcons.ERROR} fa-xl'
            break
    return *icons, *addresses, *no_update


@app.callback(Output('sensor_count', 'children'),
              [Output(f'check_{sensor.name}', 'disabled') for sensor in SetupConsts.DS_TEMP],
              Output('scan_board', 'disabled'), State('config_board', 'is_open'),
              Input('read_board', 'n_intervals'), Input('refresh_board', 'n_clicks'), prevent_initial_call=True)
def read_board(is_open, *args):
    if not realtime.in_types() or not is_open:
        raise PreventUpdate
    success = realtime.send_command(realtime.thread.events.scan_sensor, Commands.SEARCH_SENSOR, 0, timeout=2)
    sensor_count = realtime.command_outputs.get(HardwarePackets.ONE_WIRE, 0) if success else -1
    scan_board = sensor_count != 4
    enable_toggle = sensor_count != 1
    if enable_toggle:
        realtime.command_outputs[HardwarePackets.SETUP] = ''
    return f'found {sensor_count} sensors', *[enable_toggle] * len(SetupConsts.DS_TEMP), scan_board


@app.callback(
    Output("config_board", "is_open"), Input('open_config_board', 'n_clicks'),
    State("config_board", "is_open"), Input('scan_board', 'n_clicks'),
    prevent_initial_call=True)
def toggle_modal(click, is_open, scan):
    if callback_context.triggered_id == 'scan_board':
        types[realtime.thread.handler_name].send_command(Commands.SCAN, 0)
        return False
    if click:
        return not is_open
    return is_open


@app.callback(
    Output("bluetooth_modal", "is_open"), Input('bluetooth_link', 'n_clicks'), State("bluetooth_modal", "is_open"),
    prevent_initial_call=True)
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
    Output("mac_button", "children"),
    Input('mac_button', 'n_clicks'),
    [State("mac_input", "value")], prevent_initial_call=True
)
def toggle_modal(click, mac_address):
    if mac_address:
        realtime.thread.connect_handler(address=mac_address)
    raise PreventUpdate


@app.callback(
    [[Output(f"{icon['icon']['id']}_label", "children"), Output(f"{icon['icon']['id']}_link", "style")] for icon in
     TagIds.Icons.INPUT_MODES], Input('url', 'pathname'),
    Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True
)
def toggle_modal(path, interval):
    path = path.strip('/')
    output = []
    if not realtime.in_types():
        raise PreventUpdate
    current = types[realtime.thread.handler_name].current
    for icon in TagIds.Icons.INPUT_MODES:
        option = NavButtons.DEFAULT
        if icon['icon']['id'] == path:
            option = NavButtons.CLICKED
            if realtime.thread.events.Finish.connect.is_set():
                option = NavButtons.CONNECTED
            elif realtime.thread.events.disconnect.is_set():
                option = NavButtons.DISCONNECTED
        message = NavButtons.OPTIONS[option]['message'].format(current=current)
        output.append([message, {'background-color': NavButtons.OPTIONS[option]['color']}])
    return output


@app.callback(Output('placeholder', 'children'), Input('upload-file', 'contents'), State('upload-file', 'filename'),
              prevent_initial_call=True)
def load_file_data(content, file_name):
    if content:
        realtime.thread.connect_handler(content=content, file_name=file_name)


@app.callback(*[Output(name + '_graph', 'figure') for name in Settings.GRAPHS],
              Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def create_graphs(toggle, interval):
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
    for sensor in Settings.SENSORS.values():
        current_values = config[sensor.label]
        updates = {key: UnitTypes.CANCEL[sensor.unit_type](value) for key, value in current_values.items() if
                   type(value) == int}
        sensor.__dict__.update(updates)


@app.callback(Output('configuration', 'data'), Input('temperature_switch', 'on'))
def load_file_data(is_celsius):
    unit_type = UnitTypes.CELSIUS if is_celsius else UnitTypes.FAHRENHEIT
    for sensor in Settings.SENSORS.values():
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
    for sensor in Settings.SENSORS.values():
        if unit_type in sensor.possible_units:
            sensor.unit_type = unit_type
    return outputs


@app.callback(Output('placeholder', 'title'), Input(TagIds.CO2_BUTTON, 'n_clicks'), State('co2_value', 'value'),
              Input(TagIds.FAN_BUTTON, 'value'), prevent_initial_call=True)
def send_command(co2_click, co2_value, fan_value):
    if not co2_click and not fan_value:
        raise PreventUpdate
    command = None
    value = None
    if callback_context.triggered_id == TagIds.CO2_BUTTON:
        command, value = Commands.SET_CO2, co2_value
    if callback_context.triggered_id == TagIds.FAN_BUTTON:
        command, value = Commands.SET_FAN, fan_value
    types[realtime.thread.handler_name].send_command(command, value)


@app.callback(Output('theme_div', 'children'), Input(ThemeSwitchAIO.ids.switch('theme'), 'value'))
def change_theme(theme):
    Theme.DAQ_THEME['dark'] = theme
    return daq.DarkThemeProvider(theme=Theme.DAQ_THEME, children=[
        html.Div(id='page', style={'display': 'flex', 'flex-direction': 'column'}),
    ])


@app.callback(Output('configuration', 'style_header'), Output('configuration', 'style_data'),
              Input(ThemeSwitchAIO.ids.switch('theme'), 'value'))
def change_theme(theme):
    color = 'white' if theme else 'black'
    style_header = {'backgroundColor': 'var(--bs-primary)', 'color': color}
    style_data = {'backgroundColor': 'var(--bs-secondary)', 'color': color}
    return style_header, style_data


@app.callback(Output('placeholder', 'lang'), Input('save_data', 'n_intervals'))
def save_temporary_file(intervals):
    if not os.path.exists('output'):
        os.mkdir('output')
    realtime.graph.to_csv(f'output/temporary.csv')
    raise PreventUpdate

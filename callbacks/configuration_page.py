import json

from dash import Output, Input, callback_context, dash, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from configurations import SetupConsts, Settings
from consts import UnitTypes, TagIds, OutputDirectory, Icons
from default import app
from handlers.consts import Commands, HardwarePackets
from realtime_data import realtime
from tabs.set_config import load_data
from utilities import load_configuration


@app.callback(
    [Output(f'check_{name}_icon', 'className') for name in SetupConsts.COMMANDS],
    [Output(f'check_{name}_address', 'children') for name in SetupConsts.COMMANDS],
    [Output(f'check_{name}', 'on') for name in SetupConsts.COMMANDS],
    Input('reset_toggles', 'n_clicks'),
    [Input(f'check_{name}', 'on') for name in SetupConsts.COMMANDS],
    prevent_initial_call=True)
def toggle_modal(reset_toggles, *args):
    trigger = callback_context.triggered_id
    empty = [''] * len(SetupConsts.COMMANDS)
    no_update = [dash.no_update] * len(SetupConsts.COMMANDS)
    if trigger == 'reset_toggles':
        return *empty, *empty, *[False] * len(SetupConsts.COMMANDS)
    icons = no_update.copy()
    addresses = no_update.copy()
    for index, sensor in enumerate(SetupConsts.COMMANDS):
        if trigger == f'check_{sensor}':
            if not args[index]:
                icons[index] = ''
                addresses[index] = ''
            else:
                success = realtime.send_command(SetupConsts.COMMANDS[sensor], 0, realtime.thread.events.set_device)
                addresses[index] = realtime.database.get(HardwarePackets.SETUP) if success else dash.no_update
                icons[index] = Icons.Css.CHECK if success else Icons.Css.ERROR
            break
    return *icons, *addresses, *no_update


@app.callback(Output('sensor_count', 'children'),
              [Output(f'check_{name}', 'disabled') for name in SetupConsts.COMMANDS],
              Output('scan_board', 'disabled'), State('config_board', 'is_open'),
              Input('read_board', 'n_intervals'), prevent_initial_call=True)
def read_board(is_open, *args):
    if not realtime.in_types() or not is_open:
        raise PreventUpdate
    success = realtime.send_command(Commands.SEARCH_SENSOR, 0, realtime.thread.events.scan_sensor, timeout=2)
    sensor_count = realtime.database.get(HardwarePackets.ONE_WIRE, 0) if success else -1
    scan_board = sensor_count != 4
    enable_toggle = sensor_count != 1
    if enable_toggle:
        realtime.database.set(HardwarePackets.SETUP, '')
    return f'found {sensor_count} sensors', *[enable_toggle] * len(SetupConsts.COMMANDS), scan_board


@app.callback(
    Output("config_board", "is_open"), Input('open_config_board', 'n_clicks'),
    State("config_board", "is_open"), Input('scan_board', 'n_clicks'),
    prevent_initial_call=True)
def toggle_modal(click, is_open, scan):
    if callback_context.triggered_id == 'scan_board':
        realtime.send_command(Commands.SCAN, 0)
        return False
    if click:
        return not is_open
    return is_open


@app.callback(Output(TagIds.TABS, 'value'), State('configuration', 'data'), Input('save_config', 'n_clicks'),
              prevent_initial_call=True)
def load_file_data(config, click):
    if not click:
        raise PreventUpdate
    config = {row['hardware_input']: row for row in config}
    with OutputDirectory.CONFIG_FILE.open(mode='w') as config_file:
        config_file.write(json.dumps(config))
    load_configuration(config)
    return 'monitor'


@app.callback(Output('configuration', 'data'), Input('temperature_switch', 'on'))
def load_file_data(is_celsius):
    unit_type = UnitTypes.CELSIUS if is_celsius else UnitTypes.FAHRENHEIT
    for sensor in Settings.SENSORS.values():
        if unit_type in sensor.possible_units:
            sensor.unit_type = unit_type
    return load_data()


@app.callback(Output('configuration', 'style_header'), Output('configuration', 'style_data'),
              Input(ThemeSwitchAIO.ids.switch('theme'), 'value'))
def change_theme(theme):
    color = 'white' if theme else 'black'
    style_header = {'backgroundColor': 'var(--bs-primary)', 'color': color}
    style_data = {'backgroundColor': 'var(--bs-secondary)', 'color': color}
    return style_header, style_data

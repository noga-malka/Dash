from dash import Output, Input, callback_context, dash, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from configurations import SetupConsts, Settings
from consts import StatusIcons, HardwarePackets, Commands, UnitTypes, TagIds
from default import app
from realtime_data import realtime
from stoppable_thread import types
from tabs.set_config import load_data


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


@app.callback(Output(TagIds.TABS, 'value'), State('configuration', 'data'), Input('save_config', 'n_clicks'),
              prevent_initial_call=True)
def load_file_data(config, click):
    if not click:
        raise PreventUpdate
    config = {row['label']: row for row in config}
    for sensor in Settings.SENSORS.values():
        current_values = config[sensor.label]
        updates = {key: UnitTypes.CANCEL[sensor.unit_type](value) for key, value in current_values.items() if
                   type(value) is int or type(value) is float}
        sensor.__dict__.update(updates)
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

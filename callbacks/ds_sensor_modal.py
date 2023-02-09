from dash import Output, Input, callback_context, dash, State
from dash.exceptions import PreventUpdate

from configurations import SetupConsts
from consts import TagIds, Icons, TagFields
from default import app
from handlers.consts import Commands, HardwarePackets
from realtime_data import realtime


@app.callback(
    [Output(f'check_{name}_icon', TagFields.CLASS_NAME) for name in SetupConsts.COMMANDS],
    [Output(f'check_{name}_address', TagFields.CHILDREN) for name in SetupConsts.COMMANDS],
    [Output(f'check_{name}', TagFields.ON) for name in SetupConsts.COMMANDS],
    Input(TagIds.Tabs.Config.RESET_TOGGLES, TagFields.CLICK),
    [Input(f'check_{name}', TagFields.ON) for name in SetupConsts.COMMANDS],
    prevent_initial_call=True)
def manage_buttons_click(reset_toggles, *args):
    trigger = callback_context.triggered_id
    empty = [''] * len(SetupConsts.COMMANDS)
    no_update = [dash.no_update] * len(SetupConsts.COMMANDS)
    if trigger == TagIds.Tabs.Config.RESET_TOGGLES:
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


@app.callback(Output(TagIds.Tabs.Config.SENSOR_STATUS, TagFields.CHILDREN),
              [Output(f'check_{name}', TagFields.DISABLED) for name in SetupConsts.COMMANDS],
              Output(TagIds.Tabs.Config.SCAN, TagFields.DISABLED), State(TagIds.Tabs.Config.MODAL, TagFields.IS_OPEN),
              Input(TagIds.Intervals.THREE_SECONDS, TagFields.INTERVAL), prevent_initial_call=True)
def check_connected_ds_sensors_count_periodically(is_open, *args):
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
    Output(TagIds.Tabs.Config.MODAL, TagFields.IS_OPEN), Input(TagIds.Tabs.Config.OPEN_MODAL, TagFields.CLICK),
    State(TagIds.Tabs.Config.MODAL, TagFields.IS_OPEN), Input(TagIds.Tabs.Config.SCAN, TagFields.CLICK),
    prevent_initial_call=True)
def toggle_ds_command_control_modal(click, is_open, *args):
    if callback_context.triggered_id == TagIds.Tabs.Config.SCAN:
        realtime.send_command(Commands.SCAN, 0)
        return False
    if click:
        return not is_open
    return is_open

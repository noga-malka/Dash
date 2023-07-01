import time

import dash_bootstrap_components as dbc
from dash import Input, Output, callback_context, State
from dash.exceptions import PreventUpdate

from consts import TagIds, Icons, TagFields, InputModes
from dash_setup import app
from handlers.consts import Commands
from mappings.handlers import TYPES
from realtime_data import realtime


@app.callback(Output(TagIds.Modals.Clean.MODAL, TagFields.IS_OPEN), State(TagIds.Modals.Clean.MODAL, TagFields.IS_OPEN),
              Input(Icons.CLEAN['id'], TagFields.CLICK),
              Input(TagIds.Modals.Clean.NO, TagFields.CLICK), Input(TagIds.Modals.Clean.YES, TagFields.CLICK),
              prevent_initial_call=True)
def toggle_modal(is_open, *args):
    if callback_context.triggered_id == TagIds.Modals.Clean.YES:
        realtime.thread.events.clean.set()
    return not is_open


@app.callback(Output(TagIds.Modals.Files.MODAL, TagFields.IS_OPEN),
              Output(TagIds.Alerts.RECORDING_ON, TagFields.IS_OPEN),
              Input(TagIds.Modals.Save.EXIT, TagFields.CLICK),
              Input(Icons.MANAGE_FILES['id'], TagFields.CLICK),
              prevent_initial_call=True)
def toggle_modal(*args):
    if realtime.is_recording():
        return False, True
    should_open = callback_context.triggered_id == Icons.MANAGE_FILES['id']
    if should_open:
        realtime.send_command(Commands.GET_FILE_LIST)
    else:
        realtime.thread.events.live_mode.set()
    return should_open, False


@app.callback(
    Output(TagIds.Modals.Bluetooth.MODAL, TagFields.IS_OPEN),
    State(TagIds.Modals.Bluetooth.MODAL, TagFields.IS_OPEN),
    State(TagIds.Modals.Bluetooth.INPUT, TagFields.VALUE), State(TagIds.Modals.Bluetooth.INPUT, TagFields.OPTIONS),
    Input(TagIds.Modals.Bluetooth.CONNECT, TagFields.CLICK), Input('bluetooth_link', TagFields.CLICK),
    prevent_initial_call=True)
def toggle_modal(is_open, mac_address, options, *args):
    if callback_context.triggered_id == TagIds.Modals.Bluetooth.CONNECT:
        if mac_address:
            realtime.thread.connect_handler(address=mac_address, label=options[mac_address])
        return False
    return not is_open


@app.callback(Output(TagIds.Modals.Bluetooth.INPUT, TagFields.OPTIONS),
              Input(TagIds.Modals.Bluetooth.SCAN, TagFields.CLICK))
def scan_for_bluetooth_addresses(clicked):
    return TYPES[InputModes.BLUETOOTH].discover()


@app.callback(Output(TagIds.Modals.LiveStream.CONNECTIONS, TagFields.CHILDREN),
              State(TagIds.Modals.LiveStream.CONNECTIONS, TagFields.CHILDREN),
              State(TagIds.Modals.LiveStream.INPUT, TagFields.VALUE),
              State(TagIds.Modals.LiveStream.INPUT_TYPE, TagFields.VALUE),
              Input(TagIds.Modals.LiveStream.ADD, TagFields.CLICK),
              Input(TagIds.Modals.LiveStream.CLEAR, TagFields.CLICK),
              prevent_initial_call=True)
def add_connection_to_list(children, comport, input_type, *args):
    if callback_context.triggered_id == TagIds.Modals.LiveStream.CLEAR:
        return []
    if comport and input_type:
        return children + [dbc.Badge(f'{comport} : {input_type}', pill=True)]
    raise PreventUpdate


@app.callback(Output(TagIds.Modals.Save.DOWNLOAD, TagFields.DATA),
              State(TagIds.Modals.Save.FILE_OPTIONS, TagFields.VALUE),
              Input(TagIds.Modals.Save.LOAD, TagFields.CLICK), prevent_initial_call=True)
def toggle_modal(file_name, click):
    realtime.database.reset_dataframes()
    realtime.thread.events.live_mode.clear()
    realtime.send_command(Commands.READ_SINGLE_FILE, file_name)
    realtime.thread.events.live_mode.wait()
    time.sleep(1)
    return dict(filename=file_name.strip('/'), content=realtime.database.file_content)

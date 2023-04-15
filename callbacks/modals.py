from datetime import datetime

import dash_bootstrap_components as dbc
from dash import Input, Output, callback_context, State
from dash.exceptions import PreventUpdate

from consts import TagIds, Icons, TagFields, InputModes
from dash_setup import app
from mappings.handlers import TYPES
from realtime_data import realtime


@app.callback(Output(TagIds.Modals.Save.MODAL, TagFields.IS_OPEN), Input(Icons.SAVE['id'], TagFields.CLICK),
              State(TagIds.Modals.Save.MODAL, TagFields.IS_OPEN))
def toggle_modal(click, is_open):
    if click:
        return not is_open
    return is_open


@app.callback(Output(TagIds.Modals.Clean.MODAL, TagFields.IS_OPEN), State(TagIds.Modals.Clean.MODAL, TagFields.IS_OPEN),
              Input(Icons.CLEAN['id'], TagFields.CLICK),
              Input(TagIds.Modals.Clean.NO, TagFields.CLICK), Input(TagIds.Modals.Clean.YES, TagFields.CLICK),
              prevent_initial_call=True)
def toggle_modal(is_open, *args):
    if callback_context.triggered_id == TagIds.Modals.Clean.YES:
        realtime.thread.events.clean.set()
    return not is_open


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


@app.callback(Output(TagIds.Modals.Save.DOWNLOAD, TagFields.DATA), Input(TagIds.Modals.Save.BUTTON, TagFields.CLICK))
def toggle_modal(click):
    creation_time = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    return dict(filename=f'output_{creation_time}.csv', content=realtime.database.to_csv())

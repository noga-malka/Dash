from datetime import datetime

import dash_bootstrap_components as dbc
from dash import Input, Output, callback_context, State
from dash.exceptions import PreventUpdate

from consts import TagIds, Icons, TagFields, InputModes
from dash_setup import app
from mappings.controls import CONTROLS
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


@app.callback(
    Output(TagIds.Modals.Serial.MODAL, TagFields.IS_OPEN), State(TagIds.Modals.Serial.INPUT, TagFields.OPTIONS),
    State(TagIds.Modals.Serial.MODAL, TagFields.IS_OPEN), State(TagIds.Modals.Serial.CONNECTIONS, TagFields.CHILDREN),
    Input(TagIds.Modals.Serial.CONNECT, TagFields.CLICK), Input('serial_link', TagFields.CLICK),
    prevent_initial_call=True)
def toggle_modal(options, is_open, connections, *args):
    if callback_context.triggered_id == TagIds.Modals.Serial.CONNECT:
        connections = dict([badge['props'][TagFields.CHILDREN].split(' : ') for badge in connections])
        realtime.thread.connect_handler(connections=connections, labels=options)
        return False
    return not is_open


@app.callback(
    [Output(input_type, TagFields.CHILDREN) for input_type in CONTROLS],
    Input(TagIds.Modals.Serial.MODAL, TagFields.IS_OPEN),
    prevent_initial_call=True)
def toggle_modal(is_open):
    if is_open:
        raise PreventUpdate
    controls = [actions['generator']().children for input_type, actions in CONTROLS.items()]
    for (index, input_type) in enumerate(CONTROLS):
        if input_type in TYPES[realtime.thread.handler_name].handlers:
            controls[index] = CONTROLS[input_type]['generator'](True).children
    return controls


@app.callback(Output(TagIds.Modals.Bluetooth.INPUT, TagFields.OPTIONS),
              Input(TagIds.Modals.Bluetooth.SCAN, TagFields.CLICK))
def scan_for_bluetooth_addresses(clicked):
    return TYPES[InputModes.BLUETOOTH].discover()


@app.callback(Output(TagIds.Modals.Serial.INPUT, TagFields.OPTIONS), Input(TagIds.Modals.Serial.SCAN, TagFields.CLICK))
def scan_for_serial_comports(clicked):
    return TYPES[InputModes.SERIAL].discover()


@app.callback(Output(TagIds.Modals.Serial.CONNECTIONS, TagFields.CHILDREN),
              State(TagIds.Modals.Serial.CONNECTIONS, TagFields.CHILDREN),
              State(TagIds.Modals.Serial.INPUT, TagFields.VALUE),
              State(TagIds.Modals.Serial.INPUT_TYPE, TagFields.VALUE),
              Input(TagIds.Modals.Serial.ADD, TagFields.CLICK), Input(TagIds.Modals.Serial.CLEAR, TagFields.CLICK),
              prevent_initial_call=True)
def add_serial_connection_to_list(children, comport, input_type, *args):
    if callback_context.triggered_id == TagIds.Modals.Serial.CLEAR:
        return []
    if comport and input_type:
        return children + [dbc.Badge(f'{comport} : {input_type}', pill=True)]
    raise PreventUpdate


@app.callback(Output(TagIds.Modals.Save.DOWNLOAD, TagFields.DATA), Input(TagIds.Modals.Save.BUTTON, TagFields.CLICK))
def toggle_modal(click):
    creation_time = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    return dict(filename=f'output_{creation_time}.csv', content=realtime.database.to_csv())

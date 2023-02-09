from dash import Input, Output, callback_context, State

from consts import TagIds, Icons, TagFields
from default import app
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
    State(TagIds.Modals.Bluetooth.MODAL, TagFields.IS_OPEN), State(TagIds.Modals.Bluetooth.INPUT, TagFields.VALUE),
    Input(TagIds.Modals.Bluetooth.CONNECT, TagFields.CLICK), Input('bluetooth_link', TagFields.CLICK),
    prevent_initial_call=True)
def toggle_modal(is_open, mac_address, *args):
    if callback_context.triggered_id == TagIds.Modals.Bluetooth.CONNECT:
        if mac_address:
            realtime.thread.connect_handler(address=mac_address)
        return False
    return not is_open


@app.callback(
    Output(TagIds.Modals.Serial.MODAL, TagFields.IS_OPEN),
    State(TagIds.Modals.Serial.MODAL, TagFields.IS_OPEN), State(TagIds.Modals.Serial.CONNECTIONS, TagFields.CHILDREN),
    Input(TagIds.Modals.Serial.CONNECT, TagFields.CLICK), Input('serial_link', TagFields.CLICK),
    prevent_initial_call=True)
def toggle_modal(is_open, connections, *args):
    if callback_context.triggered_id == TagIds.Modals.Serial.CONNECT:
        connections = [badge['props'][TagFields.CHILDREN].split(' : ') for badge in connections]
        connections = {comport: input_type for (comport, input_type) in connections}
        realtime.thread.connect_handler(connections=connections)
        return False
    return not is_open

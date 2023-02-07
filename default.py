import bluetooth
from dash import Dash, Input, Output, callback_context, ALL, State
from dash.exceptions import PreventUpdate

from consts import TagIds, Theme, NavButtons
from layout import generate_layout
from realtime_data import realtime
from stoppable_thread import types

app = Dash(__name__, external_stylesheets=[Theme.DARK], suppress_callback_exceptions=True, title='Caeli')
app.layout = generate_layout()


@app.callback(Output('mac_input', 'options'), Input('scan_bluetooth', 'n_clicks'))
def scan_bluetooth(clicked):
    devices = {name: mac for (mac, name) in bluetooth.discover_devices(lookup_names=True)}
    if not realtime.in_types():
        raise PreventUpdate
    types[realtime.thread.handler_name].devices = devices
    return list(devices.keys())


@app.callback(Output({'type': 'icon', 'index': ALL}, 'style'),
              Input({'type': 'icon', 'index': ALL}, 'n_clicks'), prevent_initial_call=True)
def click_navigation_bar_buttons(button):
    clicked = callback_context.triggered_id['index']
    colors = [None if clicked != icon['id'] else 'red' for icon in TagIds.Icons.ALL]
    return [{'color': value} for value in colors]


@app.callback(
    Output("bluetooth_modal", "is_open"),
    Input('bluetooth_link', 'n_clicks'), State("bluetooth_modal", "is_open"),
    Input('mac_button', 'n_clicks'), State("mac_input", "value"),
    prevent_initial_call=True)
def toggle_modal(click, is_open, connect_click, mac_address):
    if callback_context.triggered_id == 'mac_button':
        if mac_address:
            realtime.thread.connect_handler(address=mac_address)
        return False
    if click:
        return not is_open
    return is_open


@app.callback(
    Output("serial_modal", "is_open"),
    Input('serial_link', 'n_clicks'), State("serial_modal", "is_open"),
    Input('serial_connect', 'n_clicks'), State("serial_input", "value"),
    prevent_initial_call=True)
def toggle_modal(click, is_open, connect_click, comport):
    if callback_context.triggered_id == 'serial_connect':
        return False
    if click:
        return not is_open
    return is_open


@app.callback(Output("save_file", "is_open"), Input({'type': 'icon', 'index': 'save'}, 'n_clicks'),
              State("save_file", "is_open"))
def toggle_modal(click, is_open):
    if click:
        return not is_open
    return is_open


@app.callback(Output("are_you_sure", "is_open"), Input({'type': 'icon', 'index': 'clean'}, 'n_clicks'),
              Input('sure_no', 'n_clicks'), Input('sure_yes', 'n_clicks'),
              [State("are_you_sure", "is_open")], prevent_initial_call=True)
def toggle_modal(clicked, no, yes, is_open):
    if callback_context.triggered_id == 'sure_yes':
        realtime.clean()
    return not is_open


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

import dash_bootstrap_components as dbc
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
    types['bluetooth'].discover()
    return list(types['bluetooth'].devices.keys())


@app.callback(Output('serial_input', 'options'), Input('scan_comports', 'n_clicks'))
def scan_comports(clicked):
    types['serial'].discover()
    return types['serial'].devices


@app.callback(Output('selected_connections', 'children'), Input('add_serial', 'n_clicks'),
              Input('clear_serial', 'n_clicks'), State('selected_connections', 'children'),
              State('serial_input', 'value'), State('input_type', 'value'), prevent_initial_call=True)
def scan_comports(add, clear, children, comport, input_type):
    if callback_context.triggered_id == 'clear_serial':
        return []
    if comport and input_type:
        return children + [dbc.Badge(f'{comport} : {input_type}', pill=True, className='me-1')]
    raise PreventUpdate


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
    Input('serial_connect', 'n_clicks'), State("selected_connections", "children"),
    prevent_initial_call=True)
def toggle_modal(click, is_open, connect_click, connections):
    if callback_context.triggered_id == 'serial_connect':
        connections = [badge['props']['children'].split(' : ') for badge in connections]
        connections = {comport: input_type for (comport, input_type) in connections}
        realtime.thread.connect_handler(connections=connections)
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
        realtime.thread.events.clean.set()
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

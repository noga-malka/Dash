import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback_context, State
from dash.exceptions import PreventUpdate

from consts import TagIds, Theme, NavButtons, InputModes
from layout import generate_layout
from realtime_data import realtime
from stoppable_thread import types

app = Dash(__name__, external_stylesheets=[Theme.DARK], suppress_callback_exceptions=True, title='Caeli')
app.layout = generate_layout()


@app.callback(Output('mac_input', 'options'), Input('scan_bluetooth', 'n_clicks'))
def scan_bluetooth(clicked):
    types[InputModes.BLUETOOTH].discover()
    return list(types[InputModes.BLUETOOTH].devices.keys())


@app.callback(Output('serial_input', 'options'), Input('scan_comports', 'n_clicks'))
def scan_comports(clicked):
    types[InputModes.SERIAL].discover()
    return types[InputModes.SERIAL].devices


@app.callback(Output('selected_connections', 'children'), Input('add_serial', 'n_clicks'),
              Input('clear_serial', 'n_clicks'), State('selected_connections', 'children'),
              State('serial_input', 'value'), State('input_type', 'value'), prevent_initial_call=True)
def scan_comports(add, clear, children, comport, input_type):
    if callback_context.triggered_id == 'clear_serial':
        return []
    if comport and input_type:
        return children + [dbc.Badge(f'{comport} : {input_type}', pill=True, className='me-1')]
    raise PreventUpdate


@app.callback(
    [[Output(f"{mode}_label", "children"), Output(f"{mode}_link", "style")] for mode in InputModes.ALL],
    Input('url', 'pathname'), Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True
)
def display_connection_status(path, *args):
    path = path.strip('/')
    output = []
    if not realtime.in_types():
        raise PreventUpdate
    current = types[realtime.thread.handler_name].current
    for input_mode in InputModes.ALL:
        option = check_status(input_mode, path)
        message = NavButtons.OPTIONS[option]['message'].format(current=current)
        output.append([message, {'background-color': NavButtons.OPTIONS[option]['color']}])
    return output


def check_status(input_mode, path):
    option = NavButtons.DEFAULT
    if input_mode == path:
        option = NavButtons.CLICKED
        if realtime.thread.events.Finish.connect.is_set():
            option = NavButtons.CONNECTED
        elif realtime.thread.events.disconnect.is_set():
            option = NavButtons.DISCONNECTED
    return option

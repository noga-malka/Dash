import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback_context, State
from dash.exceptions import PreventUpdate

from consts import TagIds, Theme, NavButtons, Icons
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


@app.callback([Output(icon['id'], 'style') for icon in Icons.ALL],
              [Input(icon['id'], 'n_clicks') for icon in Icons.ALL], prevent_initial_call=True)
def click_navigation_bar_buttons(*buttons):
    colors = [None if callback_context.triggered_id != icon['id'] else 'red' for icon in Icons.ALL]
    return [{'color': value} for value in colors]


@app.callback(
    [[Output(f"{icon['icon']['id']}_label", "children"), Output(f"{icon['icon']['id']}_link", "style")] for icon in
     Icons.INPUT_MODES], Input('url', 'pathname'),
    Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True
)
def toggle_modal(path, interval):
    path = path.strip('/')
    output = []
    if not realtime.in_types():
        raise PreventUpdate
    current = types[realtime.thread.handler_name].current
    for icon in Icons.INPUT_MODES:
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

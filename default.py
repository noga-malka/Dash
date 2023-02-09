from dash import Dash, Input, Output
from dash.exceptions import PreventUpdate

from consts import TagIds, Theme, NavButtons, InputModes, TagFields
from layout import generate_layout
from realtime_data import realtime
from stoppable_thread import types

app = Dash(__name__, external_stylesheets=[Theme.DARK], suppress_callback_exceptions=True, title='Caeli')
app.layout = generate_layout()


@app.callback(
    [[Output(f"{mode}_label", TagFields.CHILDREN), Output(f"{mode}_link", TagFields.STYLE)] for mode in InputModes.ALL],
    Input(TagIds.LOCATION, 'pathname'), Input(TagIds.Intervals.ONE_SECOND, TagFields.INTERVAL),
    prevent_initial_call=True
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

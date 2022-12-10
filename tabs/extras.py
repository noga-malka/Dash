import dash_bootstrap_components as dbc
from dash import dcc, html

from consts import Commands, TagIds
from utilities import modal_generator


def bluetooth_extra():
    inputs = [dbc.Input(id='mac_input', style={'width': 'auto'}), dbc.Button('Connect', id='mac_button')]
    modal = modal_generator('bluetooth_modal', 'Enter Mac Address', inputs)
    button = dbc.Button(id='toggle_bluetooth', children='Connect To Bluetooth',
                        style={'padding': '10px', 'margin': '5px'})
    return [button, modal]


def file_extra():
    return [dcc.Upload(id='upload-file', children=html.Div(['Drag and Drop']))]


def command_modal():
    inputs = [
        dcc.Dropdown(Commands.ALL, id='command_menu', value=Commands.ALL[0]),
        dbc.Input(id='command_input', value=Commands.COMMAND_DEFAULT.get(Commands.ALL[0]),
                  style={'width': 'auto'}),
    ]
    return modal_generator('modal', 'Command Sender', inputs, is_centered=False)


EXTRA = {
    TagIds.Icons.UPLOAD['id']: [dcc.Upload(id='upload-file', children=html.Div(['Drag and Drop']))],
    TagIds.Icons.BLUETOOTH['id']: bluetooth_extra()
}

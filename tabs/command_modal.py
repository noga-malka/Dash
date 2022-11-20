import dash_bootstrap_components as dbc
from dash import html, dcc

from consts import Commands


def command_modal():
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(html.H3("Command Sender")),
                    dbc.ModalBody([
                        dcc.Dropdown(Commands.ALL, id='command_menu', value=Commands.ALL[0]),
                        dbc.Input(id='command_input', value=Commands.COMMAND_DEFAULT.get(Commands.ALL[0]),
                                  style={'width': 'auto'}),
                        dbc.Button('Send Command', id='send_command'),
                    ], className='center align children-margin'),
                ],
                id="modal", centered=True
            ),
        ]
    )

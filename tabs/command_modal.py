import dash_bootstrap_components as dbc
from dash import html, dcc

from consts import Commands


def command_modal():
    inputs = [
        dcc.Dropdown(Commands.ALL, id='command_menu', value=Commands.ALL[0]),
        dbc.Input(id='command_input', value=Commands.COMMAND_DEFAULT.get(Commands.ALL[0]),
                  style={'width': 'auto'}),

    ]
    return modal_generator('modal', 'Command Sender', 'send_command', 'Send Command', inputs)


def modal_generator(modal_id: str, title: str, button_id: str, button_text: str, inputs: list, is_open=False):
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(html.H3(title)),
                    dbc.ModalBody([
                        *inputs,
                        dbc.Button(button_text, id=button_id),
                    ], className='center align children-margin'),
                ],
                id=modal_id, centered=True, is_open=is_open
            ),
        ]
    )

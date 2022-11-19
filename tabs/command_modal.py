import dash_bootstrap_components as dbc
from dash import html


def command_modal():
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(html.H3("Command Sender")),
                    dbc.ModalBody([]),
                ],
                id="modal", centered=True
            ),
        ]
    )

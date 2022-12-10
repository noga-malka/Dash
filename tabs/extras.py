import dash_bootstrap_components as dbc
from dash import dcc, html

from consts import TagIds
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
        html.Div(
            dbc.Button('Reset CO2 sensors', id='set_co2'),
        ),
        html.Div([
            dbc.Button('Change fan speed', id='set_fan'),
            dcc.Slider(0, 100, value=50, id='fan_slider', tooltip={'placement': 'bottom', 'always_visible': True},
                       className='full-width'),
        ], style={'width': '100%'}, className='flex align')

    ]
    return modal_generator('modal', 'Command Sender', inputs, is_centered=False)


EXTRA = {
    TagIds.Icons.UPLOAD['id']: [dcc.Upload(id='upload-file', children=html.Div(['Drag and Drop']))],
    TagIds.Icons.BLUETOOTH['id']: bluetooth_extra()
}

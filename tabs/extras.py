import dash_bootstrap_components as dbc
from dash import dcc, html

from consts import TagIds
from utilities import modal_generator


def bluetooth_extra():
    inputs = [
        dcc.Loading(children=[dcc.Dropdown(options=[], id='mac_input', className='full-width')]),
        dbc.Button('Search', id='scan_bluetooth'), dbc.Button('Connect', id='mac_button')]
    modal = modal_generator('bluetooth_modal', 'Enter Mac Address', inputs, is_centered=False)
    button = dbc.Button(id='toggle_bluetooth', children='Connect To Bluetooth',
                        style={'padding': '10px', 'margin': '5px'})
    return [button, modal, *serial_extra()]


def file_extra():
    return [dcc.Upload(id='upload-file', children=html.Div(['Drag and Drop']))]


def serial_extra():
    return [html.Div([
        dbc.Button('Reset CO2 sensors', id=TagIds.CO2_BUTTON),
        html.Div([
            html.Label('Change Fan Speed'),
            dcc.Slider(0, 100, id=TagIds.FAN_BUTTON, tooltip={'placement': 'bottom', 'always_visible': True},
                       className='full-width'),
        ], style={'width': '50%'}, className='column flex align')
    ], className='flex align children-margin center')]


def download_session():
    return modal_generator('save_file', 'Download Session',
                           [dcc.Download(id='download_text'), dbc.Button('Download csv', id='save_session')])


def are_you_sure():
    return modal_generator('are_you_sure', 'Are You Sure?',
                           [html.Div([dbc.Button('No', id='sure_no'), dbc.Button('Yes', id='sure_yes')],
                                     className='flex children-margin')])


EXTRA = {
    TagIds.Icons.UPLOAD['id']: file_extra(),
    TagIds.Icons.BLUETOOTH['id']: bluetooth_extra(),
    TagIds.Icons.SERIAL['id']: serial_extra()
}

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html

from configurations import SetupConsts
from consts import TagIds, Commands
from utilities import modal_generator


def bluetooth_extra():
    inputs = [
        dcc.Loading(children=[dcc.Dropdown(options=[], id='mac_input', className='full-width')]),
        dbc.Button('Search', id='scan_bluetooth'), dbc.Button('Connect', id='mac_button')]
    modal = modal_generator('bluetooth_modal', 'Enter Mac Address', inputs, is_centered=False)
    return [modal, *serial_extra()]


def file_extra():
    return [dcc.Upload(id='upload-file', children=html.Div(['Drag and Drop']))]


def serial_extra():
    return [html.Div([
        dbc.Button('Reset CO2 sensors', id=TagIds.CO2_BUTTON),
        dbc.Input(value=Commands.COMMAND_DEFAULT[Commands.SET_CO2], id='co2_value', style={'width': '10rem'},
                  type='number'),
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


def configurate_board():
    rows = []
    for sensor in SetupConsts.DS_TEMP:
        rows.append(html.Div([
            html.Label(sensor.name),
            daq.BooleanSwitch(id=f'check_{sensor.name}'),
            html.Div(style={'margin': '5px'}, id=f'check_{sensor.name}_icon'),
            html.Label(id=f'check_{sensor.name}_address'),
        ], className='flex children-margin align'))
    container = html.Div([html.Div(rows), dbc.Button('scan sensor', id='scan_board', disabled=True)],
                         id='board_configurator', className='flex column center')
    return modal_generator('config_board', 'Set board sensors',
                           [dcc.Loading(container)])


EXTRA = {
    TagIds.Icons.UPLOAD['id']: file_extra(),
    TagIds.Icons.BLUETOOTH['id']: bluetooth_extra(),
    TagIds.Icons.SERIAL['id']: serial_extra()
}

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html

from configurations import SetupConsts, Settings
from consts import TagIds, Commands
from utilities import modal_generator


def bluetooth_modal():
    inputs = [
        dcc.Loading(children=[dcc.Dropdown(options=[], id='mac_input', className='full-width')]),
        dbc.Button('Search', id='scan_bluetooth'), dbc.Button('Connect', id='mac_button')]
    return modal_generator('bluetooth_modal', 'Enter Mac Address', inputs, is_centered=False)


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
    labels = columnize([html.Label(Settings.SENSORS[name].group) for name in SetupConsts.DS_INPUT])
    toggles = columnize(
        [daq.BooleanSwitch(id=f'check_{name}', disabled=True) for name in SetupConsts.DS_INPUT])
    status = columnize([html.Div([html.Div(style={'margin': '5px'}, id=f'check_{name}_icon'),
                                  html.Label(id=f'check_{name}_address')]) for name in SetupConsts.DS_INPUT])

    rows = html.Div([labels, toggles, dcc.Loading(status)], className='flex space-between')
    container = html.Div([rows, generate_setup_buttons()], id='board_configurator', className='flex column center')
    return modal_generator('config_board', 'Set board sensors',
                           [
                               html.H5(id='sensor_count'),
                               container,
                               dcc.Interval('read_board', interval=3000)])


def columnize(components):
    return html.Div(components, className='flex column children-margin-2')


def generate_setup_buttons():
    return html.Div([dbc.Button('rescan board', id='refresh_board'),
                     dbc.Button('reset toggles', id='reset_toggles'),
                     dbc.Button('scan sensors', id='scan_board', disabled=True)],
                    className='flex align children-margin')


EXTRA = {
    TagIds.Icons.UPLOAD['id']: file_extra(),
    TagIds.Icons.BLUETOOTH['id']: serial_extra(),
    TagIds.Icons.SERIAL['id']: serial_extra()
}

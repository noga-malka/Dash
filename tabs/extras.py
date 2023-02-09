import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html

from configurations import SetupConsts, Settings
from consts import TagIds, Icons
from handlers.consts import InputTypes, Commands
from utilities import modal_generator, corner_radius


def bluetooth_modal():
    inputs = [
        dcc.Loading(children=[dcc.Dropdown(options=[], id=TagIds.Modals.Bluetooth.INPUT, className='full-width')]),
        dbc.Button('Search', id=TagIds.Modals.Bluetooth.SCAN),
        dbc.Button('Connect', id=TagIds.Modals.Bluetooth.CONNECT)
    ]
    return modal_generator(TagIds.Modals.Bluetooth.MODAL, 'Enter Mac Address', inputs, is_centered=False)


def serial_modal():
    inputs = [
        html.Div(id=TagIds.Modals.Serial.CONNECTIONS, children=[]),
        html.Div(
            [
                html.Div(dcc.Loading(children=[dcc.Dropdown(options=[], id=TagIds.Modals.Serial.INPUT)])),
                dcc.Dropdown(options=list(InputTypes.MAPPING), id=TagIds.Modals.Serial.INPUT_TYPE),
            ], className='flex children-margin-2 flex-grow'),
        dbc.Button('Search Ports', id=TagIds.Modals.Serial.SCAN),
        html.Div(
            [
                dbc.Button('Add Connection', id=TagIds.Modals.Serial.ADD),
                dbc.Button('Clear All', id=TagIds.Modals.Serial.CLEAR),
            ], className='flex flex-grow children-margin-2'),
        dbc.Button('Connect', id=TagIds.Modals.Serial.CONNECT)
    ]
    return modal_generator(TagIds.Modals.Serial.MODAL, 'Select Serial Connections', inputs, is_centered=False)


def file_extra():
    return [dcc.Upload(id='upload-file', children=html.Div(['Drag and Drop']))]


def generate_card(title: str, content: list):
    return html.Div([
        html.Label(title),
        html.Hr(),
        html.Div(content, className='flex center align children-margin-2')
    ], style={'padding': '10px', 'border-right': 'solid'} | corner_radius('bottom', 'right') | corner_radius('top',
                                                                                                             'right'))


def control_panel(buttons: list):
    return [
        html.Div(
            [
                dbc.Collapse([html.Div(buttons, className='flex align children-margin center')],
                             id="control_panel", className='full-width'),
                html.Div(id='expand_panel', className=Icons.Css.DOWN, style={'padding': '10px'})
            ],
            className='flex center column align bg-info',
            style=corner_radius('bottom', 'right', '50px') | corner_radius('bottom', 'left', '50px'))
    ]


def serial_extra():
    return control_panel([
        generate_card('Change DPC Mode', [
            dbc.RadioItems(id='dpc_mode_selector',
                           options=[{"label": command.title(), "value": command} for command in
                                    Commands.CO2Controller.MAPPING])]),
        generate_card('Set Point in DPC', [
            dcc.Slider(0, 2.5, id='sp_slider', disabled=True,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
        html.Div(style={'flex-grow': '1'}),
        generate_card('Reset CO2 sensors',
                      [dbc.Input(id='co2_value', type='number', style={'width': '100px'}),
                       dbc.Button('reset', id=TagIds.CO2_BUTTON)]),
        generate_card('Change Fan Speed', [
            dcc.Slider(0, 100, id=TagIds.FAN_BUTTON,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
    ])


def bluetooth_extra():
    return control_panel([
        generate_card('Reset CO2 sensors',
                      [dbc.Input(id='co2_value', type='number', style={'width': '100px'}),
                       dbc.Button('reset', id=TagIds.CO2_BUTTON)]),
        generate_card('Change Fan Speed', [
            dcc.Slider(0, 100, id=TagIds.FAN_BUTTON,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
    ])


def download_session():
    return modal_generator(TagIds.Modals.Save.MODAL, 'Download Session',
                           [
                               dcc.Download(id=TagIds.Modals.Save.DOWNLOAD),
                               dbc.Button('Download csv', id=TagIds.Modals.Save.BUTTON)
                           ])


def are_you_sure():
    buttons = [
        html.Div(
            [dbc.Button('No', id=TagIds.Modals.Clean.NO), dbc.Button('Yes', id=TagIds.Modals.Clean.YES)],
            className='flex children-margin')
    ]
    return modal_generator(TagIds.Modals.Clean.MODAL, 'Are You Sure?', buttons)


def configurate_board():
    labels = columnize([html.Label(Settings.SENSORS[name].group) for name in SetupConsts.COMMANDS])
    toggles = columnize(
        [daq.BooleanSwitch(id=f'check_{name}', disabled=True) for name in SetupConsts.COMMANDS])
    status = columnize([html.Div([html.Div(style={'margin': '5px'}, id=f'check_{name}_icon'),
                                  html.Label(id=f'check_{name}_address')]) for name in SetupConsts.COMMANDS])

    rows = html.Div([labels, toggles, dcc.Loading(status)], className='flex space-between')
    container = html.Div([rows, generate_setup_buttons()], id='board_configurator', className='flex column center')
    return modal_generator('config_board', 'Set board sensors',
                           [
                               html.H5(id='sensor_count'),
                               container,
                               dcc.Interval(**TagIds.Intervals.create_interval(TagIds.Intervals.THREE_SECONDS)),
                           ])


def columnize(components):
    return html.Div(components, className='flex column children-margin-2')


def generate_setup_buttons():
    return html.Div([dbc.Button('reset toggles', id='reset_toggles'),
                     dbc.Button('scan sensors', id='scan_board', disabled=True)],
                    className='flex align children-margin')


EXTRA = {
    Icons.UPLOAD['id']: file_extra(),
    Icons.BLUETOOTH['id']: bluetooth_extra(),
    Icons.SERIAL['id']: serial_extra()
}

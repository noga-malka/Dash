import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html

from configurations import SetupConsts, Settings
from consts import TagIds
from mappings.controls import CONTROLS
from utilities import modal_generator


def serial_modal():
    inputs = [
        html.Div(id=TagIds.Modals.LiveStream.CONNECTIONS, children=[]),
        html.Div(
            [
                html.Div(dcc.Loading(children=[dcc.Dropdown(options=[], id=TagIds.Modals.LiveStream.INPUT)])),
                dcc.Dropdown(options=list(CONTROLS), id=TagIds.Modals.LiveStream.INPUT_TYPE),
            ], className='flex children-margin-2 flex-grow'),
        dbc.Button('Search Ports', id=TagIds.Modals.LiveStream.SCAN),
        html.Div(
            [
                dbc.Button('Add Connection', id=TagIds.Modals.LiveStream.ADD),
                dbc.Button('Clear All', id=TagIds.Modals.LiveStream.CLEAR),
            ], className='flex flex-grow children-margin-2'),
        dbc.Button('Connect', id=TagIds.Modals.LiveStream.CONNECT)
    ]
    return modal_generator(TagIds.Modals.LiveStream.MODAL, 'Select Serial Connections', inputs, is_centered=False)


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
    container = html.Div([rows, generate_setup_buttons()], className='flex column center')
    return modal_generator('config_board', 'Set board sensors',
                           [
                               html.H5(id=TagIds.Tabs.Config.SENSOR_STATUS),
                               container,
                               dcc.Interval(**TagIds.Intervals.create_interval(TagIds.Intervals.THREE_SECONDS)),
                           ])


def columnize(components):
    return html.Div(components, className='flex column children-margin-2')


def generate_setup_buttons():
    return html.Div([dbc.Button('reset toggles', id=TagIds.Tabs.Config.RESET_TOGGLES),
                     dbc.Button('scan sensors', id=TagIds.Tabs.Config.SCAN, disabled=True)],
                    className='flex align children-margin')

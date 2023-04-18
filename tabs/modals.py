import dash_bootstrap_components as dbc
from dash import dcc, html

from consts import TagIds
from utilities import modal_generator


def bluetooth_modal():
    inputs = [
        dcc.Loading(children=[dcc.Dropdown(options=[], id=TagIds.Modals.Bluetooth.INPUT, className='full-width')]),
        dbc.Button('Search', id=TagIds.Modals.Bluetooth.SCAN),
        dbc.Button('Connect', id=TagIds.Modals.Bluetooth.CONNECT)
    ]
    return modal_generator(TagIds.Modals.Bluetooth.MODAL, 'Enter Mac Address', inputs, is_centered=False)


def download_session():
    return modal_generator(TagIds.Modals.Files.MODAL, 'Choose File',
                           [
                               dcc.RadioItems(id=TagIds.Modals.Save.FILE_OPTIONS),
                               dcc.Loading([
                                   dcc.Download(id=TagIds.Modals.Save.DOWNLOAD),
                                   html.Div([
                                       dbc.Button('Download File', id=TagIds.Modals.Save.LOAD),
                                   ], className='flex center align children-margin-2')
                               ])
                           ])


def are_you_sure():
    buttons = [
        html.Div(
            [dbc.Button('No', id=TagIds.Modals.Clean.NO), dbc.Button('Yes', id=TagIds.Modals.Clean.YES)],
            className='flex children-margin')
    ]
    return modal_generator(TagIds.Modals.Clean.MODAL, 'Are You Sure?', buttons)


def columnize(components):
    return html.Div(components, className='flex column children-margin-2')


def generate_setup_buttons():
    return html.Div([dbc.Button('reset toggles', id=TagIds.Tabs.Config.RESET_TOGGLES),
                     dbc.Button('scan sensors', id=TagIds.Tabs.Config.SCAN, disabled=True)],
                    className='flex align children-margin')

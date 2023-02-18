import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html

from consts import TagIds
from handlers.consts import Commands
from utilities import corner_radius


def generate_card(title: str, content: list):
    return html.Div([
        html.Label(title),
        html.Hr(),
        html.Div(content, className='flex center align children-margin-2')
    ], style={'padding': '10px', 'border-right': 'solid'} | corner_radius('bottom', 'right') | corner_radius('top',
                                                                                                             'right'))


def serial_extra():
    return [
        generate_card('Change DPC Mode', [
            dbc.RadioItems(id=TagIds.Tabs.Monitors.Control.DPC,
                           options=[{"label": command.title(), "value": command} for command in
                                    Commands.CO2Controller.MAPPING])]),
        generate_card('Set Point in DPC', [
            dcc.Slider(0, 2.5, id=TagIds.Tabs.Monitors.Control.SP_SLIDER, disabled=True,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
        html.Div(style={'flex-grow': '1'}),
        *sensors_controllers(),
    ]


def bluetooth_extra():
    return sensors_controllers()


def sensors_controllers():
    return [
        generate_card('Activate Engine',
                      [daq.BooleanSwitch(id=TagIds.Tabs.Monitors.Control.ENGINE)]),
        generate_card('Engine Speed', [
            dcc.Slider(60, 360, id=TagIds.Tabs.Monitors.Control.ENGINE_SPEED,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
        generate_card('Reset CO2 sensors',
                      [dbc.Input(id=TagIds.Tabs.Monitors.Control.CO2_VALUE, type='number',
                                 style={'width': '100px'}, value=400),
                       dbc.Button('reset', id=TagIds.Tabs.Monitors.Control.CO2)]),
        generate_card('Change Fan Speed', [
            dcc.Slider(0, 100, id=TagIds.Tabs.Monitors.Control.FAN,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
    ]


def file_extra():
    return [dcc.Upload(id=TagIds.Tabs.Monitors.UPLOAD_FILE, children=html.Div(['Drag and Drop'], className='upload'))]

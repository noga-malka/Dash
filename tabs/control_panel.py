import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html

from consts import TagIds, Icons
from handlers.consts import Commands, InputTypes


def corner_radius(is_bottom: bool = True, is_right: bool = True, size='20px'):
    vertical = 'bottom' if is_bottom else 'top'
    horizontal = 'right' if is_right else 'left'
    return {f'border-{vertical}-{horizontal}-radius': size}


def generate_card(title: str, content: list):
    return html.Div([
        html.Label(title),
        html.Hr(),
        html.Div(content, className='flex center align children-margin-2')
    ], style={'padding': '10px', 'border-right': 'solid'} | corner_radius(is_bottom=False) | corner_radius())


def controls(input_type):
    def decorator(function):
        def inner(is_connected: bool = False):
            content = function() if is_connected else generate_card(f'Input "{input_type}" - Not Connected', [])
            return html.Div(content, id=input_type, className='flex')

        return inner

    return decorator


@controls(InputTypes.CO2_CONTROLLER)
def dpc_controls():
    return [
        generate_card('Change DPC Mode', [
            dbc.RadioItems(id=TagIds.Tabs.Monitors.Control.DPC,
                           options=[{"label": command.title(), "value": command} for command in
                                    Commands.CO2Controller.COMMANDS])]),
        generate_card('Set Point in DPC', [
            dcc.Slider(0, 2.5, id=TagIds.Tabs.Monitors.Control.SP_SLIDER, disabled=True,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
    ]


@controls(InputTypes.SENSORS)
def sensors_controls():
    return [
        generate_card('Activate Engine',
                      [html.Label('Off'), daq.BooleanSwitch(id=TagIds.Tabs.Monitors.Control.ENGINE), html.Label('On')]),
        generate_card('Breath Depth', [
            dcc.Slider(60, 360, id=TagIds.Tabs.Monitors.Control.BREATH_DEPTH,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
        generate_card('Breath Rate', [
            dcc.Slider(50, 150, id=TagIds.Tabs.Monitors.Control.BREATH_RATE,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
        generate_card('Reset CO2 sensors',
                      [dbc.Input(id=TagIds.Tabs.Monitors.Control.CO2_VALUE, type='number',
                                 style={'width': '80px'}, value=400),
                       dbc.Button('reset', id=TagIds.Tabs.Monitors.Control.CO2)]),
        generate_card('Change Fan Speed', [
            dcc.Slider(0, 100, id=TagIds.Tabs.Monitors.Control.FAN,
                       tooltip={'placement': 'bottom', 'always_visible': True},
                       className='slider')]),
    ]


def live_stream_extra():
    return [sensors_controls(), dpc_controls()]


def file_extra():
    return [dcc.Upload(id=TagIds.Tabs.Monitors.UPLOAD_FILE, children=html.Div(['Drag and Drop'], className='upload'))]


def create_control_panel():
    return html.Div(
        [
            dbc.Collapse(
                [html.Div(id=TagIds.Layout.EXTRA, className='flex align children-margin space-around')],
                id=TagIds.Tabs.Monitors.Control.PANEL, className='full-width'),
            html.Div(id=TagIds.Tabs.Monitors.Control.TOGGLE_PANEL, children=Icons.Css.DOWN)
        ],
        className='flex center column align bg-info',
        style=corner_radius(size='50px') | corner_radius(is_right=False, size='50px'))

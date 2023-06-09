import dash_bootstrap_components as dbc
from dash import dcc, html

from consts import TagIds, Icons
from handlers.consts import InputTypes


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


@controls(InputTypes.SENSORS)
def sensors_controls():
    return [
        generate_card('Set Fan (RPS)', [dbc.Input(id=TagIds.Tabs.Monitors.Control.FAN_VALUE, type='number',
                                                  style={'width': '80px'}, value=0, max=270, min=0),
                                        dbc.Button('set', id=TagIds.Tabs.Monitors.Control.SET_FAN)]),
        generate_card('Set Device ID',
                      [dbc.Input(id=TagIds.Tabs.Monitors.Control.DEVICE_ID_VALUE, type='number',
                                 style={'width': '80px'}, value=0, max=65535, min=0),
                       dbc.Button('set', id=TagIds.Tabs.Monitors.Control.SET_DEVICE_ID)]),
        generate_card('Reset Counters', [dbc.Button('Reset', id=TagIds.Tabs.Monitors.Control.RESET_COUNTERS)]),
        generate_card('Delete SD files', [dbc.Button('Delete', id=TagIds.Tabs.Monitors.Control.CLEAR_SD)]),
        generate_card('Read Timers', [dbc.Button('Read', id=TagIds.Tabs.Monitors.Control.READ_TIME)]),
        generate_card('Read Clock', [dbc.Button('Read', id=TagIds.Tabs.Monitors.Control.READ_CLOCK)]),
        generate_card('Sync Clock', [dbc.Button('Sync', id=TagIds.Tabs.Monitors.Control.SYNC_CLOCK)]),
        generate_card('Read Software Version',
                      [dbc.Button('Read', id=TagIds.Tabs.Monitors.Control.READ_SOFTWARE_VERSION)]),
        generate_card('Read Device ID', [dbc.Button('Read', id=TagIds.Tabs.Monitors.Control.READ_DEVICE_ID)]),
    ]


def live_stream_extra():
    return [sensors_controls(True)]


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

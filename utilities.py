import sys

import dash_bootstrap_components as dbc
from dash import html, Output

from configurations import Sensor, Settings
from daq_functions import generate_monitor
from handlers.bluethooth_reader import BluetoothHandler
from handlers.random_handler import RandomHandler
from handlers.serial_reader import SerialHandler


def generate_grid(components):
    grid = []
    for group in components:
        row = dbc.Row(
            [dbc.Col(element, className='space-between', style={'flex-direction': 'column', 'align-items': 'center'})
             for element in group]
        )
        grid.append(row)
    return grid


def create_card(group=''):
    sensors = Settings.GROUPS[group]
    return generate_grid([[generate_monitor(field, sensors[field]) for field in sensors]])


def activate_live():
    types = {'serial': SerialHandler, 'bluetooth': BluetoothHandler, 'random': RandomHandler}
    types.get(sys.argv[1], RandomHandler)().run()


def generate_color(value, sensor: Sensor):
    return [value, value, '#ABE2FB' if sensor.low < value < sensor.high else 'red']


def generate_sensor_output(key):
    return [Output(key, 'value'), Output(key + '_led', 'value'), Output(key + '_led', 'color')]


def generate_monitor_dashboard():
    return html.Div(id='content', children=[dbc.Card(
        [
            dbc.CardHeader(group, className='center card-title'),
            dbc.CardBody(create_card(group)),
            dbc.CardFooter(id=group + '_time', className='center')
        ], className='sensor-card') for group in Settings.GROUPS],
                    className='children-margin')

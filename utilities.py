import dash_bootstrap_components as dbc
import pandas
from dash import html, Output

from configurations import Sensor, Settings
from consts import TagIds
from daq_functions import generate_monitor
from handlers.bluethooth_reader import BluetoothHandler
from handlers.random_handler import RandomHandler
from handlers.serial_reader import SerialHandler


def generate_grid(components):
    grid = []
    for group in components:
        row = dbc.Row(
            [dbc.Col(element, className='space-between', style={'flex-direction': 'column', 'align-items': 'center'})
             for element in group])
        grid.append(row)
    return grid


def create_card(group=''):
    sensors = Settings.GROUPS[group]
    return generate_grid([[generate_monitor(field, sensors[field]) for field in sensors]])


def activate_live(handler):
    types = {'serial': SerialHandler, 'bluetooth': BluetoothHandler, 'random': RandomHandler}
    return types.get(handler, RandomHandler)().extract_data


def generate_color(value, sensor: Sensor):
    is_valid = sensor.low < value < sensor.high
    icon = f'{TagIds.Icons.CHECK} valid' if is_valid else f'{TagIds.Icons.WARNING} invalid'
    return [value, value, '#ABE2FB' if is_valid else 'red', f'fa {icon}']


def generate_sensor_output(key):
    return [Output(key, 'value'), Output(key + '_led', 'value'), Output(key + '_led', 'color'),
            Output(key + '_icon', 'className')]


def generate_monitor_dashboard():
    return html.Div(id='content', children=[dbc.Card(
        [
            dbc.CardHeader(group, className='center card-title'),
            dbc.CardBody(create_card(group)),
            dbc.CardFooter(id=group + '_time', className='center')
        ], className='sensor-card') for group in Settings.GROUPS],
                    className='children-margin')


def parse_time(datetime, time_format='%H:%M:%S'):
    return pandas.Timestamp(datetime).strftime(time_format)

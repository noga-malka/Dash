import dash_bootstrap_components as dbc
import pandas
from dash import Output, html

from configurations import Sensor, Settings
from consts import TagIds
from daq_functions import generate_monitor


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


def generate_color(value, sensor: Sensor):
    is_valid = sensor.low < value < sensor.high
    icon = f'{TagIds.Icons.CHECK} valid' if is_valid else f'{TagIds.Icons.WARNING} invalid'
    color = '#ABE2FB' if is_valid else 'red'
    return [value, color, value, color, f'fa {icon}']


def generate_sensor_output(key):
    return [Output(key, 'value'), Output(key, 'color'), Output(key + '_led', 'value'), Output(key + '_led', 'color'),
            Output(key + '_icon', 'className')]


def parse_time(datetime, start):
    total = (pandas.Timestamp(datetime) - pandas.Timestamp(start)).seconds
    parsed = map(lambda number: '{:0>2}'.format(int(number)), [(total / 3600) % 60, (total / 60) % 60, total % 60])
    return ':'.join(parsed).replace('00:', '')


def modal_generator(modal_id: str, title: str, button_id: str, button_text: str, inputs: list, is_open=False):
    return html.Div([
        dbc.Modal([
            dbc.ModalHeader(html.H3(title)),
            dbc.ModalBody([*inputs, dbc.Button(button_text, id=button_id)],
                          className='center align children-margin')], id=modal_id, centered=True, is_open=is_open)]
    )

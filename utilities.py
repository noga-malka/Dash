import dash_bootstrap_components as dbc
import pandas
from dash import html

from configurations import Settings


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
    return generate_grid([[Settings.TYPES[sensor.label].generate_daq(field) for field, sensor in sensors.items()]])


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


def generate_sensors_output():
    outputs = []
    for name, sensor in Settings.SENSORS.items():
        outputs += Settings.TYPES[sensor.label].generate_output_list(name)
    return outputs

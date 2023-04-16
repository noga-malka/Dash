import dash_bootstrap_components as dbc
import pandas
import serial
from dash import html

from configurations import Settings, Schema, group_sensors, logger
from consts import UnitTypes
from handlers.handler_exception import DisconnectionEvent
from handlers.packetBuilders.sensors_builder import SensorsPacketBuilder


def generate_grid(components):
    grid = []
    for group in components:
        row = dbc.Row(
            [dbc.Col(element, className='flex column align space-between') for element in group],
            style={'height': '100%'})
        grid.append(row)
    return grid


def create_card(group=''):
    sensors = group_sensors()[group]
    return generate_grid(
        [[Schema.MONITOR_TYPES[sensor.label].generate_daq(sensor, field) for field, sensor in sensors.items()]])


def parse_time(datetime, start):
    total = (pandas.Timestamp(datetime) - pandas.Timestamp(start)).seconds
    parsed = map(lambda number: '{:0>2}'.format(int(number)), [(total / 3600) % 60, (total / 60) % 60, total % 60])
    return ':'.join(parsed).replace('00:', '')


def modal_generator(modal_id: str, title: str, inputs: list, is_centered=True):
    class_name = f'flex {"align" if is_centered else ""} center children-margin'
    return html.Div([
        dbc.Modal([
            dbc.ModalHeader(html.H3(title)),
            dbc.ModalBody([*inputs],
                          className=class_name, style={'flex-direction': 'column'})], id=modal_id, centered=True)]
    )


def generate_sensors_output():
    return [Schema.MONITOR_TYPES[sensor.label].generate_output_list(name) for name, sensor in Settings.SENSORS.items()]


def load_configuration(config: dict):
    for name, sensor in Settings.SENSORS.items():
        current_values = config[name]
        for key, value in current_values.items():
            if key in Schema.NUMERIC_FIELDS:
                current_values[key] = UnitTypes.get_converter(current_values['unit_type'], cancel=True)(value)
        sensor.__dict__.update(current_values)


def packet_sender(function):
    def inner(self, command, content):
        packet = None
        try:
            packet = SensorsPacketBuilder().build_packet(command, content)
            function(self, packet)
            logger.info(f'successfully sent packet: {packet}')
        except KeyError:
            logger.warning(f'no handler with command {command}')
        except AttributeError:
            logger.warning(f'no connection. could not send {packet}')
        except (serial.SerialException, ConnectionAbortedError):
            raise DisconnectionEvent(self.__class__.__name__)

    return inner

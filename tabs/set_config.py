import dash_bootstrap_components as dbc
from dash import dash_table
from dash import html

from configurations import Sensor, Schema, Settings
from consts import UnitTypes
from tabs.extras import configurate_board


class ConfigPage:
    @staticmethod
    def render():
        return [dbc.Button(children='Config Board', id='open_config_board'),
                html.Div(children=[
                    configurate_board(),
                    dbc.Card(
                        [
                            dbc.CardHeader('Configurations', className='flex center card-title'),
                            dbc.CardBody(dash_table.DataTable(
                                id='configuration',
                                columns=(create_columns()),
                                data=[],
                                editable=True,
                                sort_action='native',
                                style_cell={'textAlign': 'left', 'padding': '10px'},
                                style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
                                style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                            )),
                            dbc.CardFooter(className='flex center',
                                           children=dbc.Button('Save Config', id='save_config', n_clicks=0))
                        ], className='sensor-card')], className='children-margin flex center')]


def create_columns():
    return [{'id': key, 'name': field['title'], 'editable': field.get('editable', True), 'type': field['content_type']}
            for key, field in Sensor.schema()['properties'].items() if key not in Schema.HIDDEN_FIELDS]


def load_data():
    numeric = {key for key, field in Schema.SENSOR_SCHEMA.items() if field.get('content_type') == 'numeric'}
    parsed_data = []
    for sensor in Settings.SENSORS.values():
        data = sensor.dict(exclude=Schema.HIDDEN_FIELDS)
        for key in numeric:
            data[key] = UnitTypes.CONVERT[sensor.unit_type](data[key])
        parsed_data.append(data)
    return parsed_data

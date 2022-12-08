import dash_bootstrap_components as dbc
from dash import dash_table
from dash import html

from configurations import Settings, Sensor
from consts import UnitTypes


class ConfigPage:
    @staticmethod
    def render():
        return [html.Div(id='content', children=dbc.Card(
            [
                dbc.CardHeader('Configurations', className='center card-title'),
                dbc.CardBody(dash_table.DataTable(
                    id='configuration',
                    columns=(create_columns()),
                    data=load_data(),
                    editable=True,
                    style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
                    style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                )),
                dbc.CardFooter(className='center', children=dbc.Button('Save Config', id='save_config', n_clicks=0))
            ], className='sensor-card'), className='children-margin')]


def create_columns():
    return [{'id': key, 'name': field['title'], 'editable': field.get('editable', True), 'type': field['content_type']}
            for key, field in Sensor.schema()['properties'].items() if key not in Settings.HIDDEN_FIELDS]


def load_data():
    numeric = {key for key, field in Settings.SENSOR_SCHEMA.items() if field.get('content_type') == 'numeric'}
    parsed_data = []
    for sensor in Settings.ALL_SENSORS:
        data = sensor.dict(exclude=Settings.HIDDEN_FIELDS)
        for key in numeric:
            data[key] = UnitTypes.CONVERT[sensor.unit_type](data[key])
        parsed_data.append(data)
    return parsed_data

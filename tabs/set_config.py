import dash_bootstrap_components as dbc
from dash import dash_table
from dash import html

from configurations import Settings, Sensor


class ConfigPage:
    @staticmethod
    def render():
        return [html.Div(id='content', children=dbc.Card(
            [
                dbc.CardHeader('Configurations', className='center card-title'),
                dbc.CardBody(dash_table.DataTable(
                    id='table-editing-simple',
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
    return [{'id': key, 'name': field['title'], 'editable': field.get('editable', True)} for key, field in
            Sensor.schema()['properties'].items()]


def load_data():
    return [sensor.dict() for sensor in Settings.ALL_SENSORS]

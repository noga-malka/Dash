import dash_bootstrap_components as dbc
from dash import html

from configurations import group_sensors
from utilities import create_card


class LivePage:

    @staticmethod
    def render():
        return [
            html.Div(id='extra'),
            html.Div(children=[dbc.Card(
                [
                    dbc.CardHeader(id=group + 'header',
                                   children=html.Label(group),
                                   className='flex center align card-title',
                                   style={'background-color': 'var(--bs-primary)'}),
                    dbc.CardBody(create_card(group)),
                ], className='sensor-card') for group in group_sensors()],
                className='children-margin flex center', style={'flex-wrap': 'wrap'})
        ]

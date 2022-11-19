import dash_bootstrap_components as dbc
from dash import html

from configurations import Settings
from utilities import create_card


class LivePage:
    @staticmethod
    def render():
        return [html.Div(id='content', children=[dbc.Card(
            [
                dbc.CardHeader(group, className='center card-title'),
                dbc.CardBody(create_card(group)),
                dbc.CardFooter(id=group + '_time', className='center')
            ], className='sensor-card') for group in Settings.GROUPS],
                         className='children-margin')]

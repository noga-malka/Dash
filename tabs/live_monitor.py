import dash_bootstrap_components as dbc
from dash import html

from configurations import Settings
from utilities import create_card


class LivePage:
    @staticmethod
    def render():
        return [html.Div(id='content', children=[dbc.Card(
            [
                dbc.CardHeader(
                    children=[group, html.I(className='fa fa-solid fa-pen', id=group + '_edit')],
                    className='space-around center align card-title', id=group),
                dbc.CardBody(create_card(group)),
            ], className='sensor-card') for group in Settings.GROUPS],
                         className='children-margin')]

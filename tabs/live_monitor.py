import dash_bootstrap_components as dbc
from dash import html, dash_table

from configurations import Settings
from utilities import create_card


class LivePage:
    def __init__(self):
        self.saved_names = {}

    def generate_title(self, group):
        return [{'id': group, 'name': self.saved_names.get(group, group), 'renamable': True}]

    def render(self):
        return [
            html.Div(id='extra'),
            html.Div(id='content', children=[dbc.Card(
                [
                    dbc.CardHeader(
                        children=[dash_table.DataTable(id=group, columns=self.generate_title(group),
                                                       style_header={'backgroundColor': 'transparent',
                                                                     'border': 'none'})],
                        className='flex center align card-title', id=group + 'header'),
                    dbc.CardBody(create_card(group)),
                ], className='sensor-card') for group in Settings.GROUPS],
                     className='children-margin')]

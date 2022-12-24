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
            *[
                html.Div(children=[dbc.Card(
                    [
                        dbc.CardHeader(id=group + 'header',
                                       children=[dash_table.DataTable(id=group, columns=self.generate_title(group),
                                                                      style_header={'backgroundColor': 'transparent',
                                                                                    'border': 'none'})],
                                       className='flex center align card-title',
                                       style={'background-color': 'var(--bs-primary)'}),
                        dbc.CardBody(create_card(group)),
                    ], className='sensor-card') for group in row],
                    className='children-margin flex center grow')
                for row in Settings.CARD_ORDER
            ]
        ]

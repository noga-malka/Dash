import plotly.express as px
from dash import dcc, html

from configurations import Settings
from consts import Theme


class GraphPage:
    @staticmethod
    def render():
        return [
            html.Div(id='graph-container', children=[
                dcc.Graph(id=name + '_graph', figure=px.line([], template=Theme.FIGURE_DARK)) for name in
                Settings.GRAPHS
            ])
        ]

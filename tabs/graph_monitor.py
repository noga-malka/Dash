from dash import dcc, html

from configurations import Settings


class GraphPage:
    @staticmethod
    def render():
        return [
            html.Div(id='graph-container', children=[
                dcc.Graph(id=name + '_graph', animate=True) for name in Settings.GROUPS
            ])
        ]

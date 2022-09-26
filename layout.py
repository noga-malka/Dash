from dash import html, dcc
from consts import Sensors, TagIds


def make_layout():
    return html.Div([
        html.Div([
            html.H1(children='Sensors'),
            dcc.Checklist(
                Sensors.ALL, labelStyle={'margin': '5px'}, id=TagIds.CHECKLIST, value=Sensors.ALL
            )
        ], style={'text-align': 'center'}),
        dcc.Tabs(id=TagIds.TABS, value='linear', children=[
            dcc.Tab(label='Linear Graph', value='linear'),
            dcc.Tab(label='Bar Graph', value='bar'),
        ]),
        dcc.Graph(id=TagIds.GRAPH),

        dcc.Interval(
            id=TagIds.INTERVAL,
            interval=1000,  # in milliseconds
            n_intervals=0
        )
    ], className="dbc")

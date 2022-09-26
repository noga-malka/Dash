from dash import html, dcc
from consts import Sensors


def make_layout():
    return html.Div([
        html.Div([
            html.H1(children='Sensors'),
            dcc.Checklist(
                Sensors.ALL, labelStyle={'margin': '5px'}, id='sensor_options', value=Sensors.ALL
            )
        ], style={'text-align': 'center'}),
        dcc.Tabs(id="tabs", value='linear', children=[
            dcc.Tab(label='Linear Graph', value='linear'),
            dcc.Tab(label='Bar Graph', value='bar'),
        ]),
        dcc.Graph(id='example-graph'),

        dcc.Interval(
            id='interval-component',
            interval=1000,  # in milliseconds
            n_intervals=0
        )
    ], className="dbc")

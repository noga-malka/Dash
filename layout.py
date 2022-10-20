from dash import html, dcc

from consts import GraphConsts, TagIds


def make_layout():
    graphs = []
    for index in range(len(GraphConsts.FIGURES)):
        graphs += [
            dcc.Graph(id=f'{TagIds.GRAPH}_{index}')
        ]
    return html.Div(
        [
            html.Div(
                [
                    html.H1(children='Sensors'),
                    html.Div(
                        [html.Button('Save Session', id='save'),
                         html.Button('Clear Session', id='clear')],
                        style={'display': 'flex', 'justify-content': 'center'}),
                    html.Div(
                        [html.P(id='save_status', style={'margin': '5px'}),
                         html.P(id='clear_status', style={'margin': '5px'})],
                        style={'display': 'flex', 'justify-content': 'center'}),
                    html.P(id='status_text'),
                    dcc.Checklist(GraphConsts.ALL, labelStyle={'margin': '5px'}, id=TagIds.CHECKLIST,
                                  value=GraphConsts.ALL),
                    dcc.Slider(1, 20, marks={i: f'{i} minutes' for i in [1, 5, 10, 15, 20]}, value=5,
                               id=TagIds.RANGE),
                ],
                style={'text-align': 'center'}),
            dcc.Tabs(id=TagIds.TABS, value='linear',
                     children=[
                         dcc.Tab(label='Linear Graph', value='linear'),
                         dcc.Tab(label='Bar Graph', value='bar'),
                     ]),
            *graphs,
            dcc.Interval(
                id=TagIds.INTERVAL,
                interval=1000,  # in milliseconds
                n_intervals=0
            )
        ],
        className="dbc")

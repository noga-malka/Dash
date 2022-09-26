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
                    dcc.Checklist(GraphConsts.ALL, labelStyle={'margin': '5px'}, id=TagIds.CHECKLIST,
                                  value=GraphConsts.ALL)
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

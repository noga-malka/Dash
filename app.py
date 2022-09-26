import random

import pandas
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from consts import Sensors
from realtime_data import realtime

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, dbc_css])

load_figure_template('SUPERHERO')


app.layout = html.Div([
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


@app.callback(Output('example-graph', 'figure'),
              Input('sensor_options', 'value'),
              Input('tabs', 'value'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(selected_sensors, tab, intervals):
    current_time = pandas.Timestamp.now()
    sample = [{'time': current_time, 'sensor': sensor, 'value': random.randint(0, 10)} for sensor in Sensors.ALL]
    realtime.add(sample)
    data = realtime.graph[realtime.graph['sensor'].isin(selected_sensors)]
    if tab == 'linear':
        fig = px.line(data, x='time', y='value', color='sensor')
    else:
        fig = px.bar(data[data['time'] == current_time], x='sensor', y='value', color='sensor')
    fig.update_yaxes(range=[0, 10])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

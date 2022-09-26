import random

import pandas
from dash import Output, Input

from consts import Sensors, DashConsts, TagIds, DataConsts
from realtime_data import realtime
import plotly.express as px
from dash import Dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

dash_app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, DashConsts.CSS])
load_figure_template('SUPERHERO')


@dash_app.callback(Output(TagIds.GRAPH, 'figure'),
                   Input(TagIds.CHECKLIST, 'value'),
                   Input(TagIds.TABS, 'value'),
                   Input(TagIds.INTERVAL, 'n_intervals'))
def update_graph_live(selected_sensors, tab, intervals):
    current_time = pandas.Timestamp.now()
    sample = [
        {DataConsts.TIME: current_time, DataConsts.SENSOR: sensor, DataConsts.VALUE: random.randint(0, 10)}
        for sensor in Sensors.ALL]
    realtime.add(sample)
    data = realtime.graph[realtime.graph[DataConsts.SENSOR].isin(selected_sensors)]
    if tab == 'linear':
        fig = px.line(data, x=DataConsts.TIME, y=DataConsts.VALUE, color=DataConsts.SENSOR)
    else:
        fig = px.bar(data[data[DataConsts.TIME] == current_time],
                     x=DataConsts.SENSOR, y=DataConsts.VALUE, color=DataConsts.SENSOR, text=DataConsts.VALUE)
    fig.update_yaxes(range=[0, 10])
    return fig

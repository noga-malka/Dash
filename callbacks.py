import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash
from dash import Output, Input
from dash_bootstrap_templates import load_figure_template

from consts import DashConsts, TagIds, DataConsts
from realtime_data import realtime

dash_app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, DashConsts.CSS])
load_figure_template('SUPERHERO')


@dash_app.callback(Output(TagIds.GRAPH, 'figure'),
                   Input(TagIds.CHECKLIST, 'value'),
                   Input(TagIds.TABS, 'value'),
                   Input(TagIds.INTERVAL, 'n_intervals'))
def update_graph_live(selected_sensors, tab, intervals):
    data = realtime.graph[realtime.graph[DataConsts.SENSOR].isin(selected_sensors)]
    if tab == 'linear':
        fig = px.line(data, x=DataConsts.TIME, y=DataConsts.VALUE, color=DataConsts.SENSOR)
    else:
        fig = px.bar(data[data[DataConsts.TIME] == data[DataConsts.TIME].max()],
                     x=DataConsts.SENSOR, y=DataConsts.VALUE, color=DataConsts.SENSOR, text=DataConsts.VALUE)
    return fig

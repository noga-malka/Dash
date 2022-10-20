import dash_bootstrap_components as dbc
import pandas
import plotly.express as px
from dash import Dash
from dash import Output, Input
from dash_bootstrap_templates import load_figure_template

from consts import DashConsts, TagIds, DataConsts, GraphConsts
from realtime_data import realtime
from utilities import get_time_now

dash_app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, DashConsts.CSS])
load_figure_template('SUPERHERO')


@dash_app.callback(*[Output(f'{TagIds.GRAPH}_{index}', 'figure') for index in range(len(GraphConsts.FIGURES))],
                   Input(TagIds.CHECKLIST, 'value'),
                   Input(TagIds.TABS, 'value'),
                   Input(TagIds.INTERVAL, 'n_intervals'),
                   Input(TagIds.RANGE, 'value'))
def update_graph_live(selected_sensors, tab, intervals, time_range):
    figures = []
    for sensors in GraphConsts.FIGURES:
        sensors = set(sensors).intersection(selected_sensors)
        data = realtime.graph[realtime.graph[DataConsts.SENSOR].isin(sensors)]
        data = data[data[DataConsts.TIME] > pandas.Timestamp.now() - pandas.Timedelta(minutes=time_range)]
        if tab == 'linear':
            fig = px.line(data, x=DataConsts.TIME, y=DataConsts.VALUE, color=DataConsts.SENSOR)
        else:
            fig = px.bar(data[data[DataConsts.TIME] == data[DataConsts.TIME].max()],
                         x=DataConsts.SENSOR, y=DataConsts.VALUE, color=DataConsts.SENSOR, text=DataConsts.VALUE)
            fig.update_traces(textfont_size=24)
        fig.update_layout(font=dict(size=18))
        figures.append(fig)
    return figures


@dash_app.callback(
    Output('save_status', 'children'),
    Input('save', 'n_clicks')
)
def save_session(n_clicks):
    if n_clicks:
        realtime.save_session()
        return f'last save: {get_time_now()}'
    return ''


@dash_app.callback(
    Output('clear_status', 'children'),
    Input('clear', 'n_clicks')
)
def clear_session(n_clicks):
    if n_clicks:
        realtime.clear_session()
        return f'last clear: {get_time_now()}'
    return ''

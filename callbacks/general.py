import os
from datetime import datetime

import dash_daq as daq
from dash import Output, Input, html, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, Theme
from default import app
from layout import pages
from realtime_data import realtime
from tabs.extras import EXTRA
from utilities import parse_time


@app.callback(Output('extra', 'children'), Input('url', 'pathname'))
def render_content(url):
    return EXTRA.get(url.strip('/'), [])


@app.callback(Output('page', 'children'), Input(TagIds.TABS, 'value'))
def render_content(tab):
    return pages[tab]['page'].render()


@app.callback(Output('url', 'search'), Input('url', 'pathname'))
def activate_reader_thread(path: str):
    path = path.strip('/')
    if realtime.thread.handler_name != path and realtime.thread.set_handler(path):
        realtime.thread.connect_handler()
    raise PreventUpdate


@app.callback(Output('placeholder', 'lang'), Input('save_data', 'n_intervals'))
def save_temporary_file(intervals):
    if not os.path.exists('output'):
        os.mkdir('output')
    realtime.graph.to_csv(f'output/temporary.csv')
    raise PreventUpdate


@app.callback(Output('theme_div', 'children'), Input(ThemeSwitchAIO.ids.switch('theme'), 'value'))
def change_theme(theme):
    Theme.DAQ_THEME['dark'] = theme
    return daq.DarkThemeProvider(theme=Theme.DAQ_THEME, children=[
        html.Div(id='page', style={'display': 'flex', 'flex-direction': 'column'}),
    ])


@app.callback(Output('timer', 'children'),
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def update_sensors(n_intervals):
    timestamp = 'Timer: '
    if len(realtime.graph):
        timestamp += parse_time(realtime.graph.iloc[-1].name, realtime.graph.iloc[0].name)
    return timestamp


@app.callback(Output("download_text", "data"), Input('save_session', 'n_clicks'))
def toggle_modal(click):
    creation_time = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    return dict(filename=f'output_{creation_time}.csv', content=realtime.graph.to_csv())


@app.callback(Output('placeholder', 'children'), Input('upload-file', 'contents'), State('upload-file', 'filename'),
              prevent_initial_call=True)
def load_file_data(content, file_name):
    if content:
        realtime.thread.connect_handler(content=content, file_name=file_name)

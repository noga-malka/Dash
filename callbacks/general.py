from datetime import datetime

import dash_daq as daq
from dash import Output, Input, html
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, Theme
from default import app
from layout import pages
from realtime_data import realtime
from tabs.extras import EXTRA


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


@app.callback(Output('theme_div', 'children'), Input(ThemeSwitchAIO.ids.switch('theme'), 'value'))
def change_theme(theme):
    Theme.DAQ_THEME['dark'] = theme
    return daq.DarkThemeProvider(theme=Theme.DAQ_THEME, children=[
        html.Div(id='page', style={'display': 'flex', 'flex-direction': 'column'}),
    ])


@app.callback(Output('timer', 'children'),
              Input(TagIds.Intervals.ONE_SECOND, 'n_intervals'), prevent_initial_call=True)
def update_sensors(n_intervals):
    timestamp = 'Timer: '
    if realtime.database.is_not_empty():
        timestamp += realtime.database.time_gap()
    return timestamp


@app.callback(Output("download_text", "data"), Input('save_session', 'n_clicks'))
def toggle_modal(click):
    creation_time = datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    return dict(filename=f'output_{creation_time}.csv', content=realtime.database.to_csv())

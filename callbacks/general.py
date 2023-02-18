import dash_daq as daq
from dash import Output, Input, html
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, Theme, TagFields, NavButtons, InputModes, Icons
from dash_setup import app
from mappings.handlers import EXTRA, TYPES
from mappings.tabs import PAGES
from realtime_data import realtime
from tabs.control_panel import create_control_panel


@app.callback(Output(TagIds.Layout.EXTRA, TagFields.CHILDREN), Input(TagIds.LOCATION, TagFields.PATH))
def render_extra_content_by_input_mode(url):
    return EXTRA.get(url.strip('/'), [])


@app.callback(Output(TagIds.Layout.CONTENT, TagFields.CHILDREN), Input(TagIds.TABS, TagFields.VALUE))
def render_content_by_tab(tab):
    return PAGES[tab][TagIds.Layout.CONTENT].render()


@app.callback(Output(TagIds.Layout.THEME, TagFields.CHILDREN),
              Input(ThemeSwitchAIO.ids.switch(TagIds.THEME), TagFields.VALUE))
def change_theme(theme):
    Theme.DAQ_THEME['dark'] = theme
    content = [create_control_panel(), html.Div(id=TagIds.Layout.CONTENT, className='flex column')]
    return daq.DarkThemeProvider(theme=Theme.DAQ_THEME, children=content)


@app.callback(Output(TagIds.CLOCK, TagFields.CHILDREN),
              Input(TagIds.Intervals.ONE_SECOND, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    timestamp = 'Timer: '
    if realtime.database.is_not_empty():
        timestamp += realtime.database.time_gap()
    return Icons.Css.TIMER, timestamp


@app.callback(
    [[Output(f"{mode}_label", TagFields.CHILDREN), Output(f"{mode}_link", TagFields.STYLE)] for mode in InputModes.ALL],
    Input(TagIds.LOCATION, TagFields.PATH), Input(TagIds.Intervals.ONE_SECOND, TagFields.INTERVAL),
    prevent_initial_call=True
)
def display_connection_status(path, *args):
    path = path.strip('/')
    output = []
    if not realtime.in_types():
        raise PreventUpdate
    current = TYPES[realtime.thread.handler_name].current
    for input_mode in InputModes.ALL:
        option = check_status(input_mode, path)
        message = NavButtons.OPTIONS[option]['message'].format(current=current)
        output.append([message, {'background-color': NavButtons.OPTIONS[option]['color']}])
    return output


def check_status(input_mode, path):
    option = NavButtons.DEFAULT
    if input_mode == path:
        option = NavButtons.CLICKED
        if realtime.thread.events.Finish.connect.is_set():
            option = NavButtons.CONNECTED
        elif realtime.thread.events.disconnect.is_set():
            option = NavButtons.DISCONNECTED
    return option

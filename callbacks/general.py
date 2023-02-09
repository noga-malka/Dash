import dash_daq as daq
from dash import Output, Input, html
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, Theme, TagFields
from default import app
from layout import pages
from realtime_data import realtime
from tabs.extras import EXTRA


@app.callback(Output(TagIds.Layout.EXTRA, TagFields.CHILDREN), Input(TagIds.LOCATION, TagFields.PATH))
def render_extra_content_by_input_mode(url):
    return EXTRA.get(url.strip('/'), [])


@app.callback(Output(TagIds.Layout.CONTENT, TagFields.CHILDREN), Input(TagIds.TABS, TagFields.VALUE))
def render_content_by_tab(tab):
    return pages[tab][TagIds.Layout.CONTENT].render()


@app.callback(Output(TagIds.Layout.THEME, TagFields.CHILDREN),
              Input(ThemeSwitchAIO.ids.switch(TagIds.THEME), TagFields.VALUE))
def change_theme(theme):
    Theme.DAQ_THEME['dark'] = theme
    content = html.Div(id=TagIds.Layout.CONTENT, className='flex column')
    return daq.DarkThemeProvider(theme=Theme.DAQ_THEME, children=content)


@app.callback(Output(TagIds.CLOCK, TagFields.CHILDREN),
              Input(TagIds.Intervals.ONE_SECOND, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    timestamp = 'Timer: '
    if realtime.database.is_not_empty():
        timestamp += realtime.database.time_gap()
    return timestamp

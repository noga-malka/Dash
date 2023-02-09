import plotly.express as px
from dash import Output, Input
from dash_bootstrap_templates import ThemeSwitchAIO

from configurations import Settings
from consts import TagIds, Theme, DatabaseReader, TagFields
from default import app
from realtime_data import realtime


@app.callback(*[Output(name + '_graph', 'figure') for name in Settings.GRAPHS],
              Input(ThemeSwitchAIO.ids.switch(TagIds.THEME), TagFields.VALUE),
              Input(TagIds.Intervals.ONE_SECOND, TagFields.INTERVAL), prevent_initial_call=True)
def create_graphs(toggle, interval):
    figures = []
    for name, sensors in Settings.GRAPHS.items():
        all_data = realtime.database.read(DatabaseReader.ALL)
        content = all_data[list(set(all_data.columns).intersection(set(sensors)))]
        graph = px.line(content, title=name, template=Theme.FIGURE_DARK if toggle else Theme.FIGURE_LIGHT)
        figures.append(graph)
    return figures

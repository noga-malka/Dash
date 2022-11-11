import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, DaqConsts

theme = {
    'dark': True,
    'detail': '#8F8DF5',
    'primary': '#349FFC',
    'secondary': '#C0D0E2',
}


def generate_layout():
    return html.Div(
        id="main-page",
        children=[
            html.H1("Caeli", id='title', className='bg-primary  bg-opacity-50 center'),
            daq.DarkThemeProvider(theme=theme, children=[
                html.Div(
                    children=[
                        daq.GraduatedBar(max=100, value=100, step=10, size=80, style={'height': '25px'},
                                         showCurrentValue=True, color=DaqConsts.GRADIENT),
                        html.Div([
                            html.I(id={'type': 'icon', 'index': icon['id']}, className=f"fa {icon['icon']} fa-xl") for
                            icon in TagIds.Icons.ALL
                        ], className='center children-margin'),
                        ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.SUPERHERO, dbc.themes.MORPH],
                                       switch_props={"persistence": True}, icons=DaqConsts.ICONS),
                    ], className='bg-info bg-opacity-50 space-between', style={'padding': '5px'}
                ),
                dcc.Tabs(id=TagIds.TABS, value='live',
                         children=[
                             dcc.Tab(label='Live Monitor Panel', value='live'),
                             dcc.Tab(label='File Monitor Panel', value='file'),
                         ]),
                html.Div(id='page'),
                dcc.Interval(id=TagIds.INTERVAL, interval=1000, n_intervals=0),
                html.Div(id='placeholder', style={'display': None})
            ]),
        ],
    )

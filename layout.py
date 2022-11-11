import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, DaqConsts, Theme

theme = {
    'dark': True,
    'detail': '#8F8DF5',
    'primary': '#349FFC',
    'secondary': '#C0D0E2',
}


def generate_layout():
    return html.Div(
        children=[
            html.H1("Caeli", id='title', className='bg-primary display-1 center'),
            dcc.Location(id="url"),
            daq.DarkThemeProvider(theme=theme, children=[
                html.Div(
                    children=[
                        daq.GraduatedBar(max=100, value=100, step=10, size=80, style={'height': '25px'},
                                         showCurrentValue=True, color=DaqConsts.GRADIENT),
                        html.Div([
                            html.I(id={'type': 'icon', 'index': icon['id']}, className=f"fa {icon['icon']} fa-xl") for
                            icon in TagIds.Icons.ALL
                        ], className='center children-margin'),
                        ThemeSwitchAIO(aio_id="theme", themes=[Theme.DARK, Theme.LIGHT],
                                       switch_props={"persistence": True}, icons=DaqConsts.ICONS),
                    ], className='bg-info space-between',
                    style={'padding': '5px', 'align-items': 'center'}
                ),
                *[dbc.Tooltip(icon['id'], target={'type': 'icon', 'index': icon['id']}, placement="top") for icon in
                  TagIds.Icons.ALL],
                html.Div([
                    html.Div(
                        [
                            html.H2("Data Input", className="display-7"),
                            html.Hr(),
                            dbc.Nav(
                                [
                                    dbc.NavLink(
                                        [html.Div(className=f"fa {icon['icon']['icon']}", style={'padding': '10px'}),
                                         icon['label']],
                                        href=f"/{icon['icon']['id']}",
                                        active="exact") for icon in TagIds.Icons.INPUT_MODES
                                ],
                                vertical=True,
                                pills=True,
                                key=f'/{TagIds.Icons.SERIAL["id"]}'
                            ),
                        ], className='side-nav'
                    ),
                    html.Div([
                        dcc.Tabs(id=TagIds.TABS, value='monitor',
                                 children=[
                                     dcc.Tab(label='Monitor Panel', value='monitor'),
                                     dcc.Tab(label='Graph Panel', value='graph'),
                                 ]),
                        html.Div(id='page'),
                        dcc.Interval(id=TagIds.INTERVAL, interval=1000, n_intervals=0),
                        html.Div(id='placeholder', style={'display': None})
                    ], style={'width': '100%'}),
                ],
                    style={'display': 'flex'}),
            ]
                                  )
        ],
    )

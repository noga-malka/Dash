import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, DaqConsts, Theme
from css_utils import spacing, width
from tabs.extras import download_session, are_you_sure
from tabs.graph_monitor import GraphPage
from tabs.live_monitor import LivePage
from tabs.set_config import ConfigPage

pages = {
    'monitor': {'label': 'Monitor Panel', 'page': LivePage()},
    'graph': {'label': 'Graph Panel', 'page': GraphPage()},
    'config': {'label': 'Configurations', 'page': ConfigPage()}
}


def generate_buttons():
    buttons = [
        dbc.Button([
            html.I(className=f"fa {icon['icon']} fa-xl", style=spacing(5, margin=True)),
            icon['id']
        ], id={'type': 'icon', 'index': icon['id']})
        for icon in TagIds.Icons.ALL
    ]
    return [html.Div([dbc.Button('Timer:', id='timer'), *buttons],
                     className='flex center children-margin-2'),
            *[dbc.Tooltip(icon['id'], target={'type': 'icon', 'index': icon['id']}, placement="top") for icon in
              TagIds.Icons.ALL],
            ]


def generate_layout():
    return html.Div(
        children=[
            html.Div(
                html.Img(src='assets/logo.png', width=120),
                className='bg-primary flex center', style=spacing(10)),
            dcc.Location(id="url"),
            daq.DarkThemeProvider(theme=Theme.DAQ_THEME, children=[
                html.Div(
                    children=[
                        html.Div([
                            html.Label('F°'),
                            daq.BooleanSwitch(id='temperature_switch', on=True),
                            html.Label('C°'),
                        ], className='flex center align children-margin-2'),
                        *generate_buttons(),
                        ThemeSwitchAIO(aio_id="theme", themes=[Theme.DARK, Theme.LIGHT],
                                       switch_props={"persistence": True}, icons=DaqConsts.ICONS),
                    ], className='bg-info space-between align', style=spacing(5)
                ),
                html.Div([
                    html.Div(
                        [
                            html.H2("Data Input", className="display-7"),
                            html.Hr(),
                            dbc.Nav(
                                [
                                    dbc.NavLink(
                                        [html.Div(className=f"fa {icon['icon']['icon']}", style=spacing(10)),
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
                                     dcc.Tab(label=pages[key]['label'], value=key) for key in pages]),
                        download_session(),
                        are_you_sure(),
                        html.Div(id='page', className='flex column'),
                        dcc.Interval(id=TagIds.INTERVAL, interval=1000, n_intervals=0),
                        html.Div(id='placeholder', style={'display': None})
                    ], style=width('100%')),
                ],
                    className='flex'),
            ]
                                  )
        ],
    )

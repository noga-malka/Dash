import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, DaqConsts, Theme, Icons, InputModes
from mappings.tabs import PAGES
from tabs.modals import download_session, are_you_sure, configurate_board, serial_modal


def generate_buttons():
    buttons = [
        dbc.Button([icon['icon'], icon['id']], id=icon['id'])
        for icon in Icons.ALL
    ]
    return [html.Div([dbc.Button([Icons.Css.TIMER, 'Timer:'], id=TagIds.CLOCK), *buttons],
                     className='flex center children-margin-2'),
            *[dbc.Tooltip(icon['id'], target=icon['id'], placement="top") for icon in Icons.ALL]]


def generate_layout():
    return html.Div(
        children=[
            html.Div(
                html.Img(src='assets/logo.png', width=120),
                className='bg-primary flex center', style={'padding': '10px'}),
            dcc.Location(id=TagIds.LOCATION),
            html.Div(
                children=[
                    html.Div([
                        Icons.Css.FAHRENHEIT,
                        daq.BooleanSwitch(id=TagIds.TEMP_SWITCH, on=True),
                        Icons.Css.CELSIUS,
                    ], className='flex center align children-margin-2'),
                    *generate_buttons(),
                    ThemeSwitchAIO(aio_id=TagIds.THEME, themes=[Theme.DARK, Theme.LIGHT],
                                   switch_props={"persistence": True}, icons=DaqConsts.ICONS),
                ], className='bg-info space-between',
                style={'padding': '5px', 'align-items': 'center'}
            ),
            html.Div([
                html.Div(
                    [
                        html.Div(html.H2("Data Input", className="display-7"), className='sidebar-header'),
                        html.Hr(),
                        dbc.Nav(
                            [dbc.NavLink(
                                [html.Div([icon['icon'], html.Span(icon['label'])]),
                                 html.Span(id=f"{input_mode}_label")],
                                href=f"/{input_mode}", id=f"{input_mode}_link",
                                active="exact") for input_mode, icon in InputModes.ALL.items()],
                            vertical=True, pills=True
                        ),
                    ], className='sidebar'
                ),
                serial_modal(),
                download_session(),
                are_you_sure(),
                configurate_board(),
                dcc.Interval(**TagIds.Intervals.create_interval(TagIds.Intervals.SAVE_TEMPORARY_FILE)),
                dcc.Interval(**TagIds.Intervals.create_interval(TagIds.Intervals.SYNC_DATA)),
                html.Div(id=TagIds.PLACEHOLDER, style={'display': None}),
                html.Div([dcc.Tabs(id=TagIds.TABS, value='monitor',
                                   children=[dcc.Tab(label=PAGES[key]['label'], value=key) for key in PAGES]),
                          html.Div(id=TagIds.Layout.THEME)],
                         style={'width': '100%'})
            ], style={'display': 'flex'}),
        ],
    )

import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html, dcc
from dash_bootstrap_templates import ThemeSwitchAIO

from consts import TagIds, DaqConsts, Theme, Icons, InputModes
from mappings.tabs import PAGES
from tabs.modals import download_session, are_you_sure, bluetooth_modal


def generate_buttons():
    buttons = []
    for icon in Icons.ALL:
        buttons += [
            dbc.Button([icon['icon'], icon['label']], id=icon['id']),
            dbc.Tooltip(icon['label'], target=icon['id'], placement="top", id=icon['id'] + '_tooltip')
        ]
    return [html.Div(buttons, className='flex center children-margin-2')]


def generate_layout():
    return html.Div(
        children=[
            html.Div(
                html.Img(src='assets/logo.png', width=120),
                className='bg-primary flex center', style={'padding': '10px'}),
            dcc.Location(id=TagIds.LOCATION),
            dbc.Alert("Press 'Stop Recording' before trying to access SD files", id=TagIds.Alerts.RECORDING_ON,
                      color="danger", dismissable=True, fade=True, is_open=False),
            html.Div(
                children=[
                    html.Div([
                        Icons.Css.FAHRENHEIT,
                        daq.BooleanSwitch(id=TagIds.TEMP_SWITCH, on=True),
                        Icons.Css.CELSIUS,
                    ], className='flex center align children-margin-2'),
                    html.Div([
                        *generate_buttons(),
                        Icons.Css.RECORD_ICON,
                    ], className='flex center align children-margin-2'),
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
                bluetooth_modal(),
                download_session(),
                are_you_sure(),
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

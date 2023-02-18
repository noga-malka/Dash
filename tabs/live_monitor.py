import dash_bootstrap_components as dbc
from dash import html

from configurations import group_sensors, Settings
from consts import TagIds, Icons
from utilities import create_card, corner_radius


class LivePage:

    def render(self):
        groups = group_sensors()
        rows = {}
        for group_name, inputs in groups.items():
            for (index, current_inputs) in enumerate(Settings.DISPLAY):
                if set(inputs).intersection(current_inputs):
                    rows.setdefault(index, [])
                    rows[index].append(group_name)
                    break
        return [
            html.Div(
                [
                    dbc.Collapse([html.Div(id=TagIds.Layout.EXTRA, className='flex align children-margin center')],
                                 id=TagIds.Tabs.Monitors.Control.PANEL, className='full-width'),
                    html.Div(id=TagIds.Tabs.Monitors.Control.TOGGLE_PANEL, className=Icons.Css.DOWN,
                             style={'padding': '10px'})
                ],
                className='flex center column align bg-info',
                style=corner_radius(size='50px') | corner_radius(is_right=False, size='50px')),
            html.Div(
                children=sum([self._build_row(row) for row in rows.values()], []),
                className='children-margin flex center', style={'flex-wrap': 'wrap'})
        ]

    @staticmethod
    def _build_card(group):
        return dbc.Card(
            [
                dbc.CardHeader(id=group + 'header',
                               children=html.Label(group),
                               className='flex center align card-title',
                               style={'background-color': 'var(--bs-primary)'}),
                dbc.CardBody(create_card(group)),
            ], className='sensor-card')

    def _build_row(self, row):
        return [*[self._build_card(group) for group in row], html.Div(className='break-row')]

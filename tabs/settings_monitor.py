import dash_bootstrap_components as dbc
from dash import html

from handlers.consts import HardwarePackets


class SettingsPage:

    def render(self):
        return html.Div([self._build_card(hardware_input) for hardware_input in HardwarePackets.DISPLAY],
                        className='children-margin flex center', style={'flex-wrap': 'wrap'})

    @staticmethod
    def _build_card(key):
        return dbc.Card(
            [
                dbc.CardHeader(children=html.Label(key),
                               className='flex center align card-title',
                               style={'background-color': 'var(--bs-primary)'}),
                dbc.CardBody(html.P('No Data', id=key)),
            ], className='sensor-card')

from consts import TagIds
from tabs.graph_monitor import GraphPage
from tabs.live_monitor import LivePage
from tabs.settings_monitor import SettingsPage

PAGES = {
    'monitor': {'label': 'Monitor Panel', TagIds.Layout.CONTENT: LivePage()},
    'graph': {'label': 'Graph Panel', TagIds.Layout.CONTENT: GraphPage()},
    'config': {'label': 'Settings', TagIds.Layout.CONTENT: SettingsPage()}
}

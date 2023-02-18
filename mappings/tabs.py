from consts import TagIds
from tabs.graph_monitor import GraphPage
from tabs.live_monitor import LivePage
from tabs.set_config import ConfigPage

PAGES = {
    'monitor': {'label': 'Monitor Panel', TagIds.Layout.CONTENT: LivePage()},
    'graph': {'label': 'Graph Panel', TagIds.Layout.CONTENT: GraphPage()},
    'config': {'label': 'Configurations', TagIds.Layout.CONTENT: ConfigPage()}
}

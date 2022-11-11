from utilities import generate_monitor_dashboard


class LivePage:
    @staticmethod
    def render():
        return [generate_monitor_dashboard()]

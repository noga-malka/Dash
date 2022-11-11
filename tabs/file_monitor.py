from dash import dcc, html

from utilities import generate_monitor_dashboard


class FilePage:
    @staticmethod
    def render():
        return [
            dcc.Upload(
                id='upload-file',
                children=html.Div(['Drag and Drop']),
            ),
            generate_monitor_dashboard()
        ]

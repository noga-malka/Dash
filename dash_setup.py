from dash import Dash

from consts import Theme
from layout import generate_layout

app = Dash(__name__, external_stylesheets=[Theme.DARK], suppress_callback_exceptions=True, title='Caeli')
app.layout = generate_layout()

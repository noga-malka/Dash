from callbacks import dash_app
from layout import make_layout


if __name__ == '__main__':
    dash_app.layout = make_layout()
    dash_app.run_server(debug=True)

from threading import Thread

from callbacks import dash_app
from layout import make_layout
from serial_reader import SerialHandler
from utilities import save_serial_data


if __name__ == '__main__':
    handler = SerialHandler()
    Thread(target=save_serial_data, args=[handler]).start()
    dash_app.layout = make_layout()
    dash_app.run_server(debug=True, use_reloader=False)

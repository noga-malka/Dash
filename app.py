from threading import Thread

from callbacks import dash_app
from handlers.bluethooth_reader import BluetoothHandler
from layout import make_layout
from utilities import save_serial_data

if __name__ == '__main__':
    # handler = SerialHandler()
    handler = BluetoothHandler()
    Thread(target=save_serial_data, args=[handler]).start()
    dash_app.layout = make_layout()
    dash_app.run_server(debug=True, use_reloader=False)

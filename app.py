import sys
from threading import Thread

from callbacks import dash_app
from handlers.bluethooth_reader import BluetoothHandler
from handlers.serial_reader import SerialHandler
from layout import make_layout
from utilities import save_serial_data

if __name__ == '__main__':
    types = {'serial': SerialHandler, 'bluetooth': BluetoothHandler}
    if len(sys.argv) == 1 or sys.argv[1] not in types:
        print('invalid handler type received')
    else:
        handler = types.get(sys.argv[1])()
        Thread(target=save_serial_data, args=[handler]).start()
        dash_app.layout = make_layout()
        dash_app.run_server(debug=True, use_reloader=False)

import sys

from webui import WebUI

from callbacks import app

if __name__ == '__main__':
    is_debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'
    if is_debug:
        app.run_server(debug=True)
    else:
        WebUI(app).run()

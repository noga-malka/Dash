from webui import WebUI

from callbacks import app
from consts import IS_DEBUG

if __name__ == '__main__':
    if IS_DEBUG:
        app.run_server(debug=True)
    else:
        WebUI(app).run()

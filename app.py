from default import app
from callbacks.configuration_page import *
from callbacks.general import *
from callbacks.live_page import *
from callbacks.graph_page import *
from consts import IS_DEBUG

if __name__ == '__main__':
    app.run_server(debug=IS_DEBUG)

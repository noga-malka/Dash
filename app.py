from callbacks import app
from consts import IS_DEBUG

if __name__ == '__main__':
    app.run_server(debug=IS_DEBUG)

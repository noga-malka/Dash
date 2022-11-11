import sys

from callbacks import app

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('invalid handler type received')
    else:
        app.run_server(debug=True)
        # WebUI(dash_app).run()

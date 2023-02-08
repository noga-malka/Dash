from callbacks.configuration_page import *
from callbacks.general import *
from callbacks.live_page import *
from consts import IS_DEBUG

if __name__ == '__main__':
    OutputDirectory.ROOT.mkdir(parents=True, exist_ok=True)
    try:
        with OutputDirectory.CONFIG_FILE.open() as config_file:
            config = json.loads(config_file.read())
        load_configuration(config)
    except (FileNotFoundError, KeyError):
        pass
    app.run_server(debug=IS_DEBUG)

import json

from dash import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import ThemeSwitchAIO

from configurations import Settings
from consts import UnitTypes, TagIds, OutputDirectory, TagFields
from default import app
from tabs.set_config import load_data
from utilities import load_configuration


@app.callback(Output(TagIds.TABS, TagFields.VALUE), State(TagIds.Tabs.Config.TABLE, TagFields.DATA),
              Input(TagIds.Tabs.Config.SAVE_TABLE, TagFields.CLICK),
              prevent_initial_call=True)
def save_configuration_in_local_file(config, click):
    if not click:
        raise PreventUpdate
    config = {row['hardware_input']: row for row in config}
    with OutputDirectory.CONFIG_FILE.open(mode='w') as config_file:
        config_file.write(json.dumps(config))
    load_configuration(config)
    return 'monitor'


@app.callback(Output(TagIds.Tabs.Config.TABLE, TagFields.DATA), Input(TagIds.TEMP_SWITCH, TagFields.ON))
def adapt_table_to_temperature_unit_type(is_celsius):
    unit_type = UnitTypes.CELSIUS if is_celsius else UnitTypes.FAHRENHEIT
    for sensor in Settings.SENSORS.values():
        if unit_type in sensor.possible_units:
            sensor.unit_type = unit_type
    return load_data()


@app.callback(Output(TagIds.Tabs.Config.TABLE, 'style_header'), Output(TagIds.Tabs.Config.TABLE, 'style_data'),
              Input(ThemeSwitchAIO.ids.switch('theme'), TagFields.VALUE))
def change_table_theme(theme):
    color = 'white' if theme else 'black'
    style_header = {'backgroundColor': 'var(--bs-primary)', 'color': color}
    style_data = {'backgroundColor': 'var(--bs-secondary)', 'color': color}
    return style_header, style_data

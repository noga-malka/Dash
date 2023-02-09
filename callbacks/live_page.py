import numpy
from dash import Input, Output, dash, State
from dash.exceptions import PreventUpdate

from configurations import Settings, Schema, group_sensors
from consts import TagIds, Colors, UnitTypes, Icons, TagFields
from dash_setup import app
from handlers.consts import Commands
from realtime_data import realtime
from utilities import generate_sensors_output


@app.callback(generate_sensors_output(),
              Input(TagIds.Intervals.ONE_SECOND, TagFields.INTERVAL), prevent_initial_call=True)
def update_sensors_data(interval):
    try:
        content = realtime.database.read()
    except IndexError:
        content = {name: sensor.minimum for name, sensor in Settings.SENSORS.items()}
    outputs = [Schema.MONITOR_TYPES[sensor.label].generate_output_values(sensor, content.get(name, numpy.NaN)) for
               name, sensor in Settings.SENSORS.items()]
    return outputs


@app.callback([Output(group + 'header', TagFields.STYLE) for group in group_sensors()],
              Input(TagIds.Intervals.ONE_SECOND, TagFields.INTERVAL))
def update_disconnected_sensors(clicked):
    try:
        content = realtime.database.read()
    except IndexError:
        raise PreventUpdate
    disconnected = {sensor for sensor in Settings.SENSORS if numpy.isnan(content.get(sensor, numpy.NaN))}
    output = []
    for group_name, sensors in group_sensors().items():
        color = 'var(--bs-primary)'
        if disconnected.intersection(sensors):
            color = Colors.DISCONNECTED.value
        output.append({'background-color': color})
    return output


@app.callback(
    Output(TagIds.Tabs.Monitors.Control.PANEL, TagFields.IS_OPEN),
    Output(TagIds.Tabs.Monitors.Control.TOGGLE_PANEL, TagFields.CLASS_NAME),
    State(TagIds.Tabs.Monitors.Control.PANEL, TagFields.IS_OPEN),
    Input(TagIds.Tabs.Monitors.Control.TOGGLE_PANEL, TagFields.CLICK), prevent_initial_call=True
)
def toggle_control_panel(is_open, *args):
    return not is_open, Icons.Css.UP if not is_open else Icons.Css.DOWN


@app.callback(
    Output(TagIds.Tabs.Monitors.Control.SP_SLIDER, TagFields.DISABLED),
    Input(TagIds.Tabs.Monitors.Control.DPC, TagFields.VALUE),
    prevent_initial_call=True)
def enable_dpc_slider_only_in_auto_mode(mode):
    if mode:
        realtime.send_command(Commands.CO2Controller.MAPPING[mode], '')
    return mode != 'auto'


@app.callback([[Output(sensor_key, TagFields.MIN), Output(sensor_key, TagFields.MAX), Output(sensor_key, 'units'),
                Output(sensor_key + '_led', TagFields.LABEL)] for sensor_key in Settings.SENSORS],
              Input(TagIds.TEMP_SWITCH, TagFields.ON))
def change_sensors_unit_type(is_celsius):
    unit_type = UnitTypes.CELSIUS if is_celsius else UnitTypes.FAHRENHEIT
    change_function = UnitTypes.get_converter(unit_type)
    outputs = []
    for name, sensor in Settings.SENSORS.items():
        changes = [dash.no_update] * 4
        if unit_type in sensor.possible_units and sensor.unit_type != unit_type:
            changes = [change_function(sensor.minimum), change_function(sensor.maximum), unit_type, unit_type]
        outputs.append(changes)
    for sensor in Settings.SENSORS.values():
        if unit_type in sensor.possible_units:
            sensor.unit_type = unit_type
    return outputs

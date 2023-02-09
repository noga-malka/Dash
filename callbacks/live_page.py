import numpy
from dash import Input, Output, dash, callback_context, State
from dash.exceptions import PreventUpdate

from configurations import Settings, Schema, group_sensors
from consts import TagIds, Colors, UnitTypes, Icons
from default import app
from handlers.consts import Commands
from realtime_data import realtime
from utilities import generate_sensors_output


@app.callback(generate_sensors_output(),
              Input(TagIds.INTERVAL, 'n_intervals'), prevent_initial_call=True)
def update_sensors(n_intervals):
    try:
        content = realtime.database.read()
    except IndexError:
        content = {name: sensor.minimum for name, sensor in Settings.SENSORS.items()}
    outputs = [Schema.MONITOR_TYPES[sensor.label].generate_output_values(sensor, content.get(name, numpy.NaN)) for
               name, sensor in Settings.SENSORS.items()]
    return outputs


@app.callback([Output(group + 'header', 'style') for group in group_sensors()], Input(TagIds.INTERVAL, 'n_intervals'))
def scan_bluetooth(clicked):
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
    Output("control_panel", "is_open"), Output('expand_panel', 'className'),
    Input("expand_panel", "n_clicks"),
    State("control_panel", "is_open"),
)
def toggle_collapse(expand_click, is_open):
    state = not is_open
    if not expand_click:
        raise PreventUpdate
    return state, Icons.Css.UP if state else Icons.Css.DOWN


@app.callback(
    Output('sp_slider', 'disabled'), Input("dpc_mode_selector", "value"), prevent_initial_call=True)
def toggle_collapse(mode):
    if mode:
        realtime.send_command(Commands.CO2Controller.MAPPING[mode], '')
    return mode != 'auto'


@app.callback([[Output(sensor_key, 'min'), Output(sensor_key, 'max'), Output(sensor_key, 'units'),
                Output(sensor_key + '_led', 'label')] for sensor_key in Settings.SENSORS],
              Input('temperature_switch', 'on'))
def change_unit_type(is_celsius):
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


@app.callback(Output('placeholder', 'title'), Input(TagIds.CO2_BUTTON, 'n_clicks'), State('co2_value', 'value'),
              Input(TagIds.FAN_BUTTON, 'value'), prevent_initial_call=True)
def send_command(co2_click, co2_value, fan_value):
    if not co2_click and not fan_value:
        raise PreventUpdate
    command = None
    value = None
    if callback_context.triggered_id == TagIds.CO2_BUTTON:
        command, value = Commands.SET_CO2, co2_value
    if callback_context.triggered_id == TagIds.FAN_BUTTON:
        command, value = Commands.SET_FAN, fan_value
    realtime.send_command(command, value)


@app.callback(Output('placeholder', 'n_clicks'), Input('sp_slider', 'value'), prevent_initial_call=True)
def send_command(sp_value):
    if sp_value:
        realtime.send_command(Commands.CO2Controller.SET_POINT, str(sp_value))

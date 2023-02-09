from dash import Input, Output, State

from consts import TagIds, TagFields, OutputDirectory
from default import app
from handlers.consts import Commands
from realtime_data import realtime


@app.callback(Output(TagIds.PLACEHOLDER, 'title'), Input(TagIds.Tabs.Monitors.Control.FAN, TagFields.VALUE),
              prevent_initial_call=True)
def send_command(fan_value):
    if fan_value is not None:
        realtime.send_command(Commands.SET_FAN, fan_value)


@app.callback(Output(TagIds.PLACEHOLDER, 'role'), Input(TagIds.Tabs.Monitors.Control.CO2, TagFields.CLICK),
              State(TagIds.Tabs.Monitors.Control.CO2_VALUE, TagFields.VALUE), prevent_initial_call=True)
def send_command(co2_click, co2_value):
    if co2_click:
        realtime.send_command(Commands.SET_CO2, co2_value)


@app.callback(Output(TagIds.PLACEHOLDER, 'n_clicks'), Input(TagIds.Tabs.Monitors.Control.SP_SLIDER, TagFields.VALUE),
              prevent_initial_call=True)
def send_command(sp_value):
    if sp_value:
        realtime.send_command(Commands.CO2Controller.SET_POINT, str(sp_value))


@app.callback(Output(TagIds.PLACEHOLDER, 'children'), Input('upload-file', 'contents'),
              State('upload-file', 'filename'), prevent_initial_call=True)
def load_file_data(content, file_name):
    if content:
        realtime.thread.connect_handler(content=content, file_name=file_name)


@app.callback(Output(TagIds.PLACEHOLDER, 'lang'), Input('save_data', 'n_intervals'))
def save_temporary_file(intervals):
    realtime.database.to_csv(OutputDirectory.TEMP_FILE)

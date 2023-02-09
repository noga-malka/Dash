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


@app.callback(Output(TagIds.PLACEHOLDER, 'children'), Input(TagIds.Tabs.Monitors.UPLOAD_FILE, 'contents'),
              State(TagIds.Tabs.Monitors.UPLOAD_FILE, 'filename'), prevent_initial_call=True)
def load_data_from_file(content, file_name):
    if content:
        realtime.thread.connect_handler(content=content, file_name=file_name)


@app.callback(Output(TagIds.PLACEHOLDER, 'lang'), Input(TagIds.Intervals.ONE_MINUTE, TagFields.INTERVAL))
def save_temporary_file(intervals):
    realtime.database.to_csv(OutputDirectory.TEMP_FILE)


@app.callback(Output(TagIds.PLACEHOLDER, 'accessKey'), Input(TagIds.LOCATION, TagFields.PATH))
def update_the_threads_handler(path: str):
    path = path.strip('/')
    if realtime.thread.handler_name != path and realtime.thread.set_handler(path):
        realtime.thread.connect_handler()

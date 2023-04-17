from dash import Input, Output, State

from consts import TagIds, TagFields, OutputDirectory
from dash_setup import app
from handlers.consts import Commands
from realtime_data import realtime


@app.callback(Output(TagIds.PLACEHOLDER, 'title'), Input(TagIds.Tabs.Monitors.Control.FAN, TagFields.VALUE),
              prevent_initial_call=True)
def send_command(fan_value):
    if fan_value is not None:
        realtime.send_command(Commands.SET_FAN, fan_value)


@app.callback(Output(TagIds.PLACEHOLDER, 'n_clicks'), Input(TagIds.Tabs.Monitors.Control.READ_TIME, TagFields.CLICK),
              prevent_initial_call=True)
def send_command(click):
    if click is not None:
        realtime.send_command(Commands.READ_ELAPSED_TIME)


@app.callback(Output(TagIds.PLACEHOLDER, 'key'),
              Input(TagIds.Tabs.Monitors.Control.RESET_COUNTERS, TagFields.CLICK),
              prevent_initial_call=True)
def send_command(click):
    if click is not None:
        realtime.send_command(Commands.RESET_COUNTERS)
        realtime.send_command(Commands.READ_ELAPSED_TIME)


@app.callback(Output(TagIds.PLACEHOLDER, 'role'), Input(TagIds.Tabs.Monitors.Control.SET_DEVICE_ID, TagFields.CLICK),
              State(TagIds.Tabs.Monitors.Control.DEVICE_ID_VALUE, TagFields.VALUE), prevent_initial_call=True)
def send_command(co2_click, device_id):
    if co2_click:
        realtime.send_command(Commands.SET_DEVICE_ID, device_id, content_length=1)


@app.callback(Output(TagIds.PLACEHOLDER, 'contentEditable'), Input(TagIds.Tabs.Monitors.Control.SEND, TagFields.CLICK),
              State(TagIds.Tabs.Monitors.Control.COMMAND, TagFields.VALUE),
              State(TagIds.Tabs.Monitors.Control.DATA, TagFields.VALUE),
              prevent_initial_call=True)
def send_command(click, command, data):
    if click and command is not None and data is not None:
        realtime.send_command(command, data)


@app.callback(Output(TagIds.PLACEHOLDER, 'children'), Input(TagIds.Tabs.Monitors.UPLOAD_FILE, 'contents'),
              State(TagIds.Tabs.Monitors.UPLOAD_FILE, 'filename'), prevent_initial_call=True)
def load_data_from_file(content, file_name):
    if content:
        realtime.thread.connect_handler(content=content, file_name=file_name)


@app.callback(Output(TagIds.PLACEHOLDER, 'lang'), Input(TagIds.Intervals.SAVE_TEMPORARY_FILE, TagFields.INTERVAL))
def save_temporary_file(intervals):
    realtime.database.to_csv(OutputDirectory.TEMP_FILE)


@app.callback(Output(TagIds.PLACEHOLDER, 'accessKey'), Input(TagIds.LOCATION, TagFields.PATH))
def update_the_threads_handler(path: str):
    path = path.strip('/')
    if realtime.thread.handler_name != path and realtime.thread.set_handler(path):
        realtime.thread.connect_handler()

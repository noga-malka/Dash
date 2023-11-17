from datetime import datetime, timedelta

from dash import Input, Output, State, callback_context

from consts import TagIds, TagFields, OutputDirectory
from dash_setup import app
from handlers.consts import Commands
from realtime_data import realtime

command_mapping = {
    TagIds.Buttons.STOP_RECORD: Commands.STOP_RECORD,
    TagIds.Tabs.Monitors.Control.READ_TIME: Commands.READ_ELAPSED_TIME,
    TagIds.Tabs.Monitors.Control.READ_CLOCK: Commands.READ_CLOCK,
    TagIds.Tabs.Monitors.Control.READ_DEVICE_ID: Commands.READ_DEVICE_ID,
    TagIds.Tabs.Monitors.Control.READ_SOFTWARE_VERSION: Commands.SOFTWARE_VERSION,
    TagIds.Tabs.Monitors.Control.CLEAR_SD: Commands.DELETE_FILES,
    TagIds.Tabs.Monitors.Control.RESET_COUNTERS: Commands.RESET_COUNTERS,
}


@app.callback(Output(TagIds.PLACEHOLDER, 'title'),
              Input(TagIds.Tabs.Monitors.Control.SET_FAN, TagFields.CLICK),
              State(TagIds.Tabs.Monitors.Control.FAN_VALUE, TagFields.VALUE),
              prevent_initial_call=True)
def send_command(click, fan_value):
    if click and fan_value:
        realtime.send_command(Commands.SET_FAN, fan_value)


@app.callback(Output(TagIds.PLACEHOLDER, 'n_clicks'),
              Input(TagIds.Buttons.STOP_RECORD, TagFields.CLICK),
              Input(TagIds.Tabs.Monitors.Control.READ_DEVICE_ID, TagFields.CLICK),
              Input(TagIds.Tabs.Monitors.Control.CLEAR_SD, TagFields.CLICK),
              Input(TagIds.Tabs.Monitors.Control.READ_TIME, TagFields.CLICK),
              Input(TagIds.Tabs.Monitors.Control.READ_CLOCK, TagFields.CLICK),
              Input(TagIds.Tabs.Monitors.Control.RESET_COUNTERS, TagFields.CLICK),
              Input(TagIds.Tabs.Monitors.Control.READ_SOFTWARE_VERSION, TagFields.CLICK),
              prevent_initial_call=True)
def send_command(*clicks):
    if any(clicks):
        realtime.send_command(command_mapping[callback_context.triggered_id])


@app.callback(Output(TagIds.PLACEHOLDER, 'draggable'), Input(TagIds.Buttons.START_RECORD, TagFields.CLICK),
              prevent_initial_call=True)
def send_command(click):
    if click is not None:
        realtime.send_command(Commands.START_RECORD, datetime.now().strftime('%Y%m%d%H%M'))


@app.callback(Output(TagIds.PLACEHOLDER, 'spellCheck'), Input(TagIds.Tabs.Monitors.Control.SYNC_CLOCK, TagFields.CLICK),
              State(TagIds.Tabs.Monitors.Control.TIME_ZONE_VALUE, TagFields.VALUE),
              prevent_initial_call=True)
def send_command(click, timezone):
    if click is not None:
        current_time = datetime.now() + timedelta(hours=timezone)
        content = current_time.strftime('%y,%m,%d,%H,%M').split(',')
        realtime.send_command(Commands.WRITE_CLOCK, content, content_length=1)


@app.callback(Output(TagIds.PLACEHOLDER, 'role'), Input(TagIds.Tabs.Monitors.Control.SET_DEVICE_ID, TagFields.CLICK),
              State(TagIds.Tabs.Monitors.Control.DEVICE_ID_VALUE, TagFields.VALUE), prevent_initial_call=True)
def send_command(co2_click, device_id):
    if co2_click:
        realtime.send_command(Commands.SET_DEVICE_ID, device_id, content_length=2)


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

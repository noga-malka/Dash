from dash import Output, Input
from dash.exceptions import PreventUpdate

from consts import TagIds, TagFields
from dash_setup import app
from handlers.consts import HardwarePackets
from realtime_data import realtime


@app.callback(Output(HardwarePackets.RUN_TIME, TagFields.CHILDREN),
              Input(TagIds.Intervals.SYNC_DATA, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    return compare_to_previous(HardwarePackets.RUN_TIME)


@app.callback(Output(HardwarePackets.TOTAL_TIME, TagFields.CHILDREN),
              Input(TagIds.Intervals.SYNC_DATA, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    return compare_to_previous(HardwarePackets.TOTAL_TIME)


@app.callback(Output(HardwarePackets.DEVICE_ID, TagFields.CHILDREN),
              Input(TagIds.Intervals.SYNC_DATA, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    return compare_to_previous(HardwarePackets.DEVICE_ID)


@app.callback(Output(HardwarePackets.SOFTWARE_VERSION, TagFields.CHILDREN),
              Input(TagIds.Intervals.SYNC_DATA, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    return compare_to_previous(HardwarePackets.SOFTWARE_VERSION)


@app.callback(Output(HardwarePackets.CLOCK, TagFields.CHILDREN),
              Input(TagIds.Intervals.SYNC_DATA, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    return compare_to_previous(HardwarePackets.CLOCK)


def compare_to_previous(key: str):
    current, changed = realtime.database.get_value(key, check_previous=True)
    if changed:
        return current
    raise PreventUpdate

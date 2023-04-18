from dash import Output, Input

from consts import TagIds, TagFields
from dash_setup import app
from handlers.consts import HardwarePackets
from realtime_data import realtime


@app.callback(Output(HardwarePackets.RUN_TIME, TagFields.CHILDREN),
              Input(TagIds.Intervals.SYNC_DATA, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    return realtime.database.single_values.get(HardwarePackets.RUN_TIME, 'No Data')


@app.callback(Output(HardwarePackets.TOTAL_TIME, TagFields.CHILDREN),
              Input(TagIds.Intervals.SYNC_DATA, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    return realtime.database.single_values.get(HardwarePackets.TOTAL_TIME, 'No Data')


@app.callback(Output(HardwarePackets.DEVICE_ID, TagFields.CHILDREN),
              Input(TagIds.Intervals.SYNC_DATA, TagFields.INTERVAL), prevent_initial_call=True)
def update_timer(intervals):
    return realtime.database.single_values.get(HardwarePackets.DEVICE_ID, 'No Data')

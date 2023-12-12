import pm4py
import pandas as pd
import datetime
from pydantic import BaseModel
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.visualization.process_tree import visualizer as pt_visualizer


def get_average_activity_times(EventLog):

    event_log = pd.read_csv(EventLog.filename, parse_dates=[EventLog.timestamp], infer_datetime_format=True)
    dataframe = pm4py.format_dataframe(event_log, case_id=EventLog.caseID, activity_key=EventLog.activity, timestamp_key=EventLog.timestamp)
    event_log = pm4py.convert_to_event_log(dataframe)
    
    average_duration_per_activity = {}
    for trace in event_log:
        for i in range(0, len(trace) - 1):
            current_activity = trace[i]['concept:name']
            next_activity = trace[i + 1]['concept:name']
            duration = (trace[i + 1]['time:timestamp'] - trace[i]['time:timestamp']).total_seconds()
            if current_activity not in average_duration_per_activity:
                average_duration_per_activity[current_activity] = []
            average_duration_per_activity[current_activity].append(duration)

    for activity in average_duration_per_activity:
        average_duration_per_activity[activity] = sum(average_duration_per_activity[activity]) / len(average_duration_per_activity[activity])
    return average_duration_per_activity
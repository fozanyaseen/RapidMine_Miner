import pm4py
import pandas as pd
import datetime
from pydantic import BaseModel
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.visualization.process_tree import visualizer as pt_visualizer



def get_process_insights(EventLogCSV):

    filenameID = EventLogCSV.filename
    caseID = EventLogCSV.caseID
    activityID = EventLogCSV.activity
    timestampID = EventLogCSV.timestamp

    event_log = pd.read_csv(filenameID, parse_dates=[timestampID], infer_datetime_format=True)
    dataframe = pm4py.format_dataframe(event_log, case_id=caseID, activity_key=activityID, timestamp_key=timestampID)
    dataframe['case_duration'] = event_log.groupby(caseID)[timestampID].transform(lambda x: x.max() - x.min())
    
    EventLog = pm4py.convert_to_event_log(dataframe)


    total_cases = len(dataframe[EventLogCSV.caseID].unique())
    formatted_total_cases = format_number(total_cases)


    average_case_duration = get_average_case_duration(dataframe)
    formatted_average_case_duration = format_time(average_case_duration.total_seconds())

    average_duration_per_activity = get_average_activity_times(EventLog)
    formatted_average_duration_per_activity = {}
    for activity in average_duration_per_activity:
        formatted_average_duration_per_activity[activity] = format_time(average_duration_per_activity[activity])

    long_cases = get_long_cases(dataframe, average_case_duration)


    critical_path_duration = get_critical_path_duration(EventLog)
    formatted_critical_path_duration = format_time(critical_path_duration)

    critical_path_activities = get_critical_path_activities(EventLog)

    sorted_case_times = sort_case_times(EventLog, caseID)
    
    return {"total_cases": formatted_total_cases, "average_case_duration": formatted_average_case_duration, "average_duration_per_activity": formatted_average_duration_per_activity, "long_cases": long_cases, "critical_path_duration": formatted_critical_path_duration, "critical_path_activities": critical_path_activities, "sorted_case_times": sorted_case_times}


def sort_case_times(EventLog, case_id):
    # Sort the traces by their total duration
    trace_durations = []
    for trace in EventLog:
        if len(trace) > 1:
            start_time = trace[0]['time:timestamp']
            end_time = trace[-1]['time:timestamp']
            duration = (end_time - start_time).total_seconds()
            trace_durations.append((duration, trace[0][case_id]))

    trace_durations.sort(key=lambda x: x[0], reverse=True)
    return trace_durations

def get_critical_path_activities(EventLog):
    trace_durations = []
    for trace in EventLog:
        if len(trace) > 1:
            start_time = trace[0]['time:timestamp']
            end_time = trace[-1]['time:timestamp']
            duration = (end_time - start_time).total_seconds()
            activities = [event['concept:name'] for event in trace]
            trace_durations.append((duration, activities))

    # Identify the trace with the longest total duration (critical path)
    if trace_durations:
        critical_path = max(trace_durations, key=lambda x: x[0])
        critical_path_activities = critical_path[1]
    else:
        critical_path_activities = []

    return critical_path_activities    



def get_critical_path_duration(EventLog):
    total_duration_per_trace = []
    for trace in EventLog:
        if len(trace) > 1:
            start_time = trace[0]['time:timestamp']
            end_time = trace[-1]['time:timestamp']
            duration = (end_time - start_time).total_seconds()
            total_duration_per_trace.append(duration)

    # Identify the longest trace (critical path)
    if total_duration_per_trace:
        longest_duration = max(total_duration_per_trace)
        critical_path_duration = longest_duration
    else:
        critical_path_duration = 0

    return critical_path_duration    




def get_average_case_duration(dataframe):
# Now you can calculate average duration and identify long cases
    avg_duration = dataframe['case_duration'].mean()
    return avg_duration

def get_long_cases(dataframe, average_case_duration):
    long_cases = dataframe[dataframe['case_duration'] > average_case_duration]
    return long_cases


def get_average_activity_times(EventLog):
    
    average_duration_per_activity = {}
    for trace in EventLog:
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

def format_number(num):
    if num < 1000:
        return str(num)
    elif 1000 <= num < 1000000:
        return f"{num/1000:.2f}K"
    elif 1000000 <= num < 1000000000:
        return f"{num/1000000:.2f}M"
    elif 1000000000 <= num < 1000000000000:
        return f"{num/1000000000:.2f}B"
    else:
        return f"{num/1000000000000:.2f}T"
    

def format_time(seconds):
    units = [
        ("day", 86400),
        ("hr", 3600),
        ("min", 60),
        ("sec", 1)
    ]

    for unit_name, unit_seconds in units:
        if seconds >= unit_seconds:
            value = seconds / unit_seconds
            if value.is_integer():
                return f"{int(value)} {unit_name}"
            else:
                return f"{value:.1f} {unit_name}"

    return f"{seconds} sec"   
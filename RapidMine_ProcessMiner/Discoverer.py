import pm4py
import pandas as pd
import datetime
from pydantic import BaseModel
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.visualization.process_tree import visualizer as pt_visualizer

def discover_process_from_csv(EventLog):
        event_log = pd.read_csv(EventLog.filename, parse_dates=[EventLog.timestamp], infer_datetime_format=True)
        dataframe = pm4py.format_dataframe(event_log, case_id=EventLog.caseID, activity_key=EventLog.activity, timestamp_key=EventLog.timestamp)
        event_log = pm4py.convert_to_event_log(dataframe)
        tree = pm4py.discover_process_tree_inductive(event_log)
        bpmn_graph = pm4py.convert_to_bpmn(tree)

        bpmnfile = f"{EventLog.filename.split('.')[0]}.bpmn"
        bpmnfile = bpmnfile.replace("Files", "output_bpmn")
        pm4py.write_bpmn(bpmn_graph, bpmnfile)
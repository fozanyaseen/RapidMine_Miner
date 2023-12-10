import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer

# Load your event log
log_path = "nasa-cev-1-10-single-trace.xes"  # Replace with the path to your event log file
log = xes_importer.apply(log_path)

# Convert log to event stream if it's not already an event stream
# if pm4py.get_properties(log)["is_tracelog"]:
# log = log_converter.apply(log, variant=log_converter.TO_EVENT_STREAM)

# Discover a process model using inductive miner
tree = pm4py.discover_process_tree_inductive(log)

# Convert the process tree to BPMN model
bpmn_graph = pm4py.convert_to_bpmn(tree)

pm4py.view_bpmn(bpmn_graph)
gviz = pt_visualizer.apply(tree)
pt_visualizer.view(gviz)

# Save the BPMN diagram
# bpmn_visualizer.save(bpmn_visualization, "bpmn_diagram.png")

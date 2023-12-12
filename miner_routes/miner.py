from fastapi import APIRouter, UploadFile, HTTPException
# import torch
import logging
from decouple import config
from fastapi.websockets import WebSocket
from fastapi.responses import JSONResponse
import json
import pm4py
import pandas as pd
import datetime
from pydantic import BaseModel
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from RapidMine_ProcessMiner import Discoverer



router = APIRouter()

class EventLog(BaseModel):
    filename: str
    columns: list
    caseID: str
    activity: str
    timestamp: str



@router.post("/get_columns")
async def get_columns(file: UploadFile):
    try:
        filename = file.filename.split(".")[0]
        extension = file.filename.split(".")[1]
        filename = f"Files\{filename}.{extension}"
        with open(filename, "wb") as buffer:
            buffer.write(file.file.read())

        dataframe = pd.read_csv(filename, sep=",")
        return {"columns": list(dataframe.keys()), "filename": filename}

    except Exception as e:
        logging.exception("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/create_bpmn")
async def create_bpmn(EventLog: EventLog):
    try:
        event_log = pd.read_csv(EventLog.filename, parse_dates=[EventLog.timestamp], infer_datetime_format=True)
        dataframe = pm4py.format_dataframe(event_log, case_id=EventLog.caseID, activity_key=EventLog.activity, timestamp_key=EventLog.timestamp)
        event_log = pm4py.convert_to_event_log(dataframe)
        tree = pm4py.discover_process_tree_inductive(event_log)
        bpmn_graph = pm4py.convert_to_bpmn(tree)

        bpmnfile = f"{EventLog.filename.split('.')[0]}.bpmn"
        bpmnfile = bpmnfile.replace("Files", "output_bpmn")
        pm4py.write_bpmn(bpmn_graph, bpmnfile)

        with open(bpmnfile, "r") as buffer:
            bpmnXML = buffer.read()
        return {"bpmn": bpmnXML}
    except Exception as e:
        logging.exception("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_insights")
async def get_insights():
    try:
        return {"average_activity_times": "average_activity_times"}
    except Exception as e:
        logging.exception("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")    







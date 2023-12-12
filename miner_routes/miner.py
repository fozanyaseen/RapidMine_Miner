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
from RapidMine_Analytics import Analytics



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
        bpmn = Discoverer.discover_process_from_csv(EventLog)
        return bpmn
    except Exception as e:
        logging.exception("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_insights")
async def get_insights(EventLog: EventLog):
    try:
        insights = Analytics.get_process_insights(EventLog)
        return insights
    except Exception as e:
        logging.exception("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")    







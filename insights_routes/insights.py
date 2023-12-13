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


@router.post("/get_insights")
async def get_insights(EventLog: EventLog):
    print(EventLog)
    try:
        insights = Analytics.get_process_insights(EventLog)
        return insights
    except Exception as e:
        logging.exception("An error occurred:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")    







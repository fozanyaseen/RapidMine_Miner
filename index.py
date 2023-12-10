# from routes import process_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from routes import process_owner_routes
# from routes import employee_routes
from miner_routes import miner

# from transcriber import transcriber
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(miner.router, prefix="/miner", tags=["Miner"])

# app.include_router(employee_routes.router, prefix="/employee", tags=["Employee"])
# app.include_router(process_routes.router, prefix="/process", tags=["Process"])
# app.include_router(process_owner_routes.router, prefix="/process-owner", tags=["Process Owner"])
# app.include_router(transcriber.router, prefix="/transcribe", tags=["Transcriber"])
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
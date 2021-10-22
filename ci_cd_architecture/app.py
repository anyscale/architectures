import os
from typing import Literal
from uuid import UUID

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from loguru import logger
from pydantic import BaseModel

from demo_lifecycle.log_config import setup_logging
from demo_lifecycle.ray_impl.remote_compute import RayEntryPoint


class ServiceStatus(BaseModel):
    status: Literal["OK", "Unhealthy"]

    class Config:
        extra = "forbid"


app = FastAPI(
    title="KGSA Predictions Service",
    description="Provides model training and prediction services",
    version=os.environ.get("IMAGE_TAG", "development"),
)


global entry_point

@app.on_event("startup")
def on_startup():
    try:
        ANYSCALE_URL = f"anyscale://demo-lifecycle-{os.environ['ANYSCALE_ENVIRONMENT']}"
    except KeyError:
        ANYSCALE_URL = f"anyscale://demo-lifecycle"
    ANYSCALE_CLI_TOKEN = os.environ["ANYSCALE_CLI_TOKEN"]
    print(f"Starting or connecting to Anyscale Cluster {ANYSCALE_URL}")
    global entry_point
    entry_point = RayEntryPoint(ANYSCALE_URL, ANYSCALE_CLI_TOKEN)

@app.on_event("shutdown")
async def on_shutdown():
    entry_point.cleanup()

# first iteration - synchronous ray task
@app.post(
    "/service/ray_submit",
    #response_model=StatusResponse,
    response_model_exclude_unset=True,
    summary="Ray Job",
    tags=["Ray"],
)
async def start_ray_job():
    entry_point.execute()
    return {"status":"Job submitted"}

@app.get(
    "/service/ray_result",
    summary="Ray Result",
    tags=["Ray"],
)
async def get_job_result():
    result = entry_point.respond()
    return {"status":str(result)}

@app.get(
    "/service/status",
    response_model=ServiceStatus,
    response_model_exclude_unset=True,
    tags=["Service"],
)
async def status():
    # TODO :: Add health checks like db connectivity
    return {"status": "OK"}


@app.get(
    "/service/healthcheck/gtg",
    response_model=ServiceStatus,
    response_model_exclude_unset=True,
    tags=["Service"],
)
async def healthcheck_gtg():
    return {"status": "OK"}


##-------------------------main------------------

setup_logging()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

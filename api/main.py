import logging
import time
import uuid

import requests
from cachetools import TTLCache
from dotenv import dotenv_values
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth

config = dotenv_values(".env")


logger = logging.getLogger("web-api-logger")
logger.setLevel(logging.DEBUG)
custom_logging_handler = LokiLoggerHandler(
    url="http://loki.loki.svc.cluster.local:3100/loki/api/v1/push",
    labels={"application": "portfolio", "component": "web-api"},
)
logger.addHandler(custom_logging_handler)


class CommandBody(BaseModel):
    command: str


class Movie(BaseModel):
    title: str


app = FastAPI()
cache = TTLCache(maxsize=15, ttl=180)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    unique_request_id = str(uuid.uuid4())
    start_time = time.time()
    method = request.method
    path = request.url.path
    query_params = dict(request.query_params)
    try:
        body = await request.body()
        body = body.decode("utf-8") if body else "empty"
    except Exception:
        body = "Body could not be parsed"

    log_string = f"{request.client.host} | {unique_request_id}: {method} | {path} {query_params} - IN PROGRESS | Body: {body}"
    logger.info(log_string)
    request.state.unique_request_id = unique_request_id

    response = await call_next(request)

    response_time = time.time() - start_time
    status_code = response.status_code
    log_string = f"{request.client.host} | {unique_request_id}: {method} | {path} {query_params} - {status_code} | Body: {body} | Response Time: {response_time:.2f}s"
    logger.info(log_string)

    return response


@app.post("/cmd")
def cmd(command_body: CommandBody, request: Request):
    logger.info(
        f"{request.client.host} | {request.state.unique_request_id}: command {command_body.command}"
    )
    res = requests.post(
        "http://portfolio-vm:5003/cmd",
        json={"command": command_body.command},
        headers={"Content-type": "application/json"},
    )
    try:
        res.raise_for_status()
    except Exception as e:
        logger.critical(
            f"{request.client.host} | {request.state.unique_request_id}: Error: {e}",
            exc_info=True,
        )

    command_result = res.json()
    logger.info(
        f"{request.client.host} | {request.state.unique_request_id}: command={command_body.command} | {command_result=}"
    )
    return command_result


@app.post("/initdag")
def init_dag(movie: Movie, request: Request):
    logger.info(
        f"{request.client.host} | {request.state.unique_request_id}: movie request -> {movie.title}"
    )
    cache_result = cache.get(movie.title)
    if cache_result:
        logger.info(
            f"{request.state.unique_request_id}: cache hit for -> {movie.title}"
        )
        return {"result": "movie request is already being processed"}
    logger.info(
        f"{request.client.host} | {request.state.unique_request_id}: cache miss for -> {movie.title}"
    )
    cache[movie.title] = "processing"
    res = requests.post(
        "http://airflow-webserver.airflow.svc.cluster.local:8080/api/v1/dags/movie_retriever_dag/dagRuns",
        headers={"Content-Type": "application/json"},
        json={"conf": {"title": movie.title}},
        auth=HTTPBasicAuth(config["AIRFLOW_USER"], config["AIRFLOW_PASSWORD"]),
    )
    try:
        res.raise_for_status()
    except Exception as e:
        logger.critical(
            f"{request.client.host} | {request.state.unique_request_id}: Error: {e}",
            exc_info=True,
        )

    return res.json()


@app.get("/health")
def health():
    res = requests.post(
        "http://portfolio-vm:5003/cmd",
        json={"command": "ls"},
        headers={"Content-type": "application/json"},
    )
    res.raise_for_status()

    command_result = res.json()

    return command_result


app.mount("/", StaticFiles(directory="../web", html=True), name="static")

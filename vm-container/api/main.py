import subprocess

from fastapi import FastAPI
from pydantic import BaseModel


class CommandBody(BaseModel):
    command: str


app = FastAPI()


@app.post("/cmd")
async def cmd(command_body: CommandBody):
    try:
        result = subprocess.run(
            command_body.command,
            capture_output=True,
            shell=True,
            executable="/bin/bash",
            timeout=15,
        )
        encoded_result = result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
        return {"result": encoded_result}
    except Exception:
        return {"result": "Network Error: Your command did not reach the host machine."}


@app.get("/health")
async def health():
    try:
        result = subprocess.run(
            "ls",
            capture_output=True,
            shell=True,
            executable="/bin/bash",
            timeout=15,
        )
        encoded_result = result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
        return {"result": encoded_result}
    except Exception:
        return {"result": "Network Error: Your command did not reach the host machine."}

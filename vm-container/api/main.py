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
            executable="/home/narrator/bin/rbash",
            user="narrator",
            group="narrator",
            env={
                "PATH": "/home/narrator/bin",  # Restrict PATH to rbash environment
                "HOME": "/home/narrator",  # Set home for the user
            },
            timeout=15,
        )
        encoded_result = result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
        return {"result": encoded_result}
    except Exception:
        raise {"result": "Network Error: Your command did not reach the host machine."}


@app.get("/health")
async def health():
    try:
        result = subprocess.run(
            "ls",
            capture_output=True,
            shell=True,
            executable="/home/narrator/bin/rbash",
            user="narrator",
            group="narrator",
            env={
                "PATH": "/home/narrator/bin",
                "HOME": "/home/narrator",
            },
            timeout=15,
        )
        encoded_result = result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
        return {"result": encoded_result}
    except Exception:
        raise {"result": "Network Error: Your command did not reach the host machine."}

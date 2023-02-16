import json
import commands.CommandExecutor as CommandExecutor
from commands.celery import app


@app.task
def commandExecute(body: str) -> None:
    payload = json.loads(body)
    CommandExecutor.CommandExecutor().execute(payload)


@app.task
def commandDelayedExecute(body: str) -> None:
    payload = json.loads(body)
    CommandExecutor.CommandExecutor().execute(payload)

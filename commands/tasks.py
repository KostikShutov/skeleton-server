import json
from commands.CommandExecutor import CommandExecutor
from commands.celery import app

commandExecutor = CommandExecutor()


@app.task
def commandExecute(body: str) -> None:
    payload: dict = json.loads(body)
    commandExecutor.execute(payload)


@app.task
def commandDelayedExecute(body: str) -> None:
    payload: dict = json.loads(body)
    commandExecutor.execute(payload)

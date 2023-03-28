import json
from commands.CommandExecutor import CommandExecutor
from commands.celery import app

commandExecutor = CommandExecutor()


@app.task
def commandTask(body: str) -> None:
    payload: dict = json.loads(body)
    commandExecutor.execute(payload)

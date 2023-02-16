import json
import commands.BackwardCommand as BackwardCommand
import commands.ForwardCommand as ForwardCommand
import commands.LeftCommand as LeftCommand
import commands.RightCommand as RightCommand
import commands.StopCommand as StopCommand
import commands.StraightCommand as StraightCommand
import commands.TurnCommand as TurnCommand
from commands.celery import app


@app.task
def commandExecute(body: str) -> None:
    commands = [
        BackwardCommand.BackwardCommand(),
        ForwardCommand.ForwardCommand(),
        LeftCommand.LeftCommand(),
        RightCommand.RightCommand(),
        StopCommand.StopCommand(),
        StraightCommand.StraightCommand(),
        TurnCommand.TurnCommand(),
    ]

    payload = json.loads(body)

    for command in commands:
        if command.canExecute(payload):
            command.execute(payload)

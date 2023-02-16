import commands.BackwardCommand as BackwardCommand
import commands.ForwardCommand as ForwardCommand
import commands.LeftCommand as LeftCommand
import commands.RightCommand as RightCommand
import commands.StopCommand as StopCommand
import commands.StraightCommand as StraightCommand
import commands.TurnCommand as TurnCommand


class CommandExecutor:
    def __init__(self):
        self.commands = [
            BackwardCommand.BackwardCommand(),
            ForwardCommand.ForwardCommand(),
            LeftCommand.LeftCommand(),
            RightCommand.RightCommand(),
            StopCommand.StopCommand(),
            StraightCommand.StraightCommand(),
            TurnCommand.TurnCommand(),
        ]

    def execute(self, payload: dict) -> None:
        for command in self.commands:
            if command.canExecute(payload):
                command.execute(payload)

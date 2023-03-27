import uuid
from commands.BackwardCommand import BackwardCommand
from commands.ForwardCommand import ForwardCommand
from commands.LeftCommand import LeftCommand
from commands.RightCommand import RightCommand
from commands.StopCommand import StopCommand
from commands.StraightCommand import StraightCommand
from commands.TurnCommand import TurnCommand
from commands.CameraLeftCommand import CameraLeftCommand
from commands.CameraRightCommand import CameraRightCommand
from commands.CameraUpCommand import CameraUpCommand
from commands.CameraDownCommand import CameraDownCommand
from controllers.ControllerResolver import ControllerResolver
from utils.Redis import redis


class CommandExecutor:
    def __init__(self) -> None:
        controller = ControllerResolver().resolve()
        controller.init()

        self.commands = [
            BackwardCommand(controller),
            ForwardCommand(controller),
            LeftCommand(controller),
            RightCommand(controller),
            StopCommand(controller),
            StraightCommand(controller),
            TurnCommand(controller),
            CameraLeftCommand(controller),
            CameraRightCommand(controller),
            CameraUpCommand(controller),
            CameraDownCommand(controller),
        ]

    def execute(self, commandId: uuid.UUID, payload: dict) -> None:
        for command in self.commands:
            if command.canExecute(payload):
                command.execute(commandId, payload)
                redis.set(name='command_' + str(commandId), value=1, ex=300)

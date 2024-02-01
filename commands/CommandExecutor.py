import logging
from commands.SpeedCommand import SpeedCommand
from commands.BackwardCommand import BackwardCommand
from commands.ForwardCommand import ForwardCommand
from commands.MoveCommand import MoveCommand
from commands.LeftCommand import LeftCommand
from commands.RightCommand import RightCommand
from commands.StopCommand import StopCommand
from commands.StraightCommand import StraightCommand
from commands.TurnCommand import TurnCommand
from commands.CameraLeftCommand import CameraLeftCommand
from commands.CameraRightCommand import CameraRightCommand
from commands.CameraUpCommand import CameraUpCommand
from commands.CameraDownCommand import CameraDownCommand
from controllers.ControllerInterface import ControllerInterface


class CommandExecutor:
    def __init__(self, controller: ControllerInterface) -> None:
        controller.init()

        self.commands = [
            SpeedCommand(controller),
            BackwardCommand(controller),
            ForwardCommand(controller),
            MoveCommand(controller),
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

    def execute(self, payload: dict) -> None:
        for command in self.commands:
            if command.canExecute(payload):
                command.execute(payload)
                return

        logging.warning('[Commander] Cannot execute command (%s)' % payload)

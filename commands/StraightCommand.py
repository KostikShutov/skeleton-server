from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class StraightCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: object) -> None:
        self.controller.straight()

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'STRAIGHT'

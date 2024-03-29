from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class RightCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        self.controller.right()

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'RIGHT'

from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class StopCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        self.controller.stop()

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'STOP'

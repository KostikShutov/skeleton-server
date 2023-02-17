from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class TurnCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: object) -> None:
        self.controller.turn(int(payload['angle']))

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'TURN'

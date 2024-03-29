from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class TurnCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        angle: int = int(payload['steering'])

        self.controller.turn(angle)

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'TURN'

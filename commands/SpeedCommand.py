from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class SpeedCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        speed: int = int(payload['speed']) if 'speed' in payload else 60

        self.controller.speed(speed)

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'SPEED'

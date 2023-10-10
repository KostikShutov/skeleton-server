import time
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class ForwardCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        speed: int = int(payload['speed']) if 'speed' in payload else 60
        duration: float = float(payload['duration']) if 'duration' in payload else 0

        self.controller.forward(speed)

        if duration > 0:
            time.sleep(duration)
            self.controller.stop()

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'FORWARD' or payload['name'] == 'MOVE'

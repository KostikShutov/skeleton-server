from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface
from utils.Utils import microSleep


class BackwardCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        speed: int = int(payload['speed']) if 'speed' in payload else None
        duration: float = float(payload['duration']) if 'duration' in payload else 0

        self.controller.backward(speed)

        if duration > 0:
            microSleep(duration)
            self.controller.stop()

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'BACKWARD'

import time
import uuid
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class BackwardCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, commandId: uuid.UUID, payload: dict) -> None:
        speed: int = int(payload['speed'])
        distance: float = float(payload['distance']) if 'distance' in payload else None
        duration: float = (payload['duration']) if 'duration' in payload else None

        if distance is not None and duration is None:
            duration: float = float(distance / speed)

        self.controller.backward(speed)

        if duration is not None:
            time.sleep(duration)
            self.controller.stop()

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'BACKWARD'

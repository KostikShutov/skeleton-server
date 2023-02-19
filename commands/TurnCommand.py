import math
import uuid
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class TurnCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, commandId: uuid.UUID, payload: dict) -> bool:
        x: float = float(payload['x']) if 'x' in payload else None
        y: float = float(payload['y']) if 'y' in payload else None

        # Todo: xy feature
        if x is not None and y is not None:
            x = max(x, 0)
            y = max(y, 0)

            if y == 0:
                angle: int = int(self.controller.state()['minAngle'])
            else:
                if x == 0:
                    angle: int = int(self.controller.state()['maxAngle'])
                else:
                    angle: int = int(
                        math.degrees(math.atan2(y, x))
                        - int(self.controller.state()['currentAngle'])
                        + 45
                        + 45
                    )
        else:
            angle: int = int(payload['angle']) if 'angle' in payload else None

        if angle is not None:
            self.controller.turn(angle)

        return True

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'TURN'

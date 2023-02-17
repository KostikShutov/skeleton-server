from commands.CommandPusher import CommandPusher
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class BackwardCommand(CommandInterface):
    def __init__(self,
                 controller: ControllerInterface,
                 commandPusher: CommandPusher) -> None:
        self.controller = controller
        self.commandPusher = commandPusher

    def execute(self, payload: dict) -> None:
        speed: int = int(payload['speed'])
        distance: int = payload['distance'] if 'distance' in payload else None
        duration: int = payload['duration'] if 'duration' in payload else None

        if duration is not None:
            self.commandPusher.pushDelayedStop(duration)

        self.controller.backward(speed, distance, duration)

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'BACKWARD'

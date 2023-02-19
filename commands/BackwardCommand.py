import uuid
from commands.CommandPusher import CommandPusher
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface
from utils.Redis import redis


class BackwardCommand(CommandInterface):
    def __init__(self,
                 controller: ControllerInterface,
                 commandPusher: CommandPusher) -> None:
        self.controller = controller
        self.commandPusher = commandPusher

    def execute(self, commandId: uuid.UUID, payload: dict) -> bool:
        speed: int = int(payload['speed'])
        distance: int = payload['distance'] if 'distance' in payload else None
        duration: int = payload['duration'] if 'duration' in payload else None

        redis.set('currentVerticalCommandId', str(commandId))

        if duration is not None:
            self.commandPusher.pushDelayedStop(commandId, duration)

        self.controller.backward(speed, distance, duration)
        return duration is None

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'BACKWARD'

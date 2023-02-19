import uuid
from commands.CommandPusher import CommandPusher
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface
from utils.Redis import redis


class ForwardCommand(CommandInterface):
    def __init__(self,
                 controller: ControllerInterface,
                 commandPusher: CommandPusher) -> None:
        self.controller = controller
        self.commandPusher = commandPusher

    def execute(self, commandId: uuid.UUID, payload: dict) -> bool:
        speed: int = int(payload['speed'])
        distance: int = int(payload['distance']) if 'distance' in payload else None
        duration: int = int(payload['duration']) if 'duration' in payload else None

        if distance is not None and duration is None:
            duration = int(distance / speed)

        redis.set('currentVerticalCommandId', str(commandId))

        if duration is not None and duration > 0:
            self.commandPusher.pushDelayedStop(commandId, duration)

        self.controller.forward(speed, distance, duration)
        return duration is None

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'FORWARD'

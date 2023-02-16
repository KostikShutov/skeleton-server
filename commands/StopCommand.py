import commands.CommandInterface as CommandInterface
import controllers.ControllerResolver as ControllerResolver
from utils.Redis import redis


class StopCommand(CommandInterface.CommandInterface):
    def __init__(self):
        self.redis = redis
        self.controller = ControllerResolver.ControllerResolver()

    def execute(self, payload: object) -> None:
        verticalCommandId: str = payload['verticalCommandId'] if 'verticalCommandId' in payload else None

        if self.needSkip(verticalCommandId):
            return

        self.redis.delete('currentVerticalCommandId')
        self.controller.resolve().stop()

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'STOP'

    def needSkip(self, verticalCommandId: str) -> bool:
        if verticalCommandId is not None:
            currentVerticalCommandId = self.redis.get('currentVerticalCommandId')

            if currentVerticalCommandId is None:
                return True

            currentVerticalCommandId: str = str(currentVerticalCommandId.decode('utf-8'))

            if verticalCommandId != currentVerticalCommandId:
                return True

        return False

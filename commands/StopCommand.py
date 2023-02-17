from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface
from utils.Redis import redis


class StopCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: object) -> None:
        verticalCommandId: str = payload['verticalCommandId'] if 'verticalCommandId' in payload else None

        if self.needSkip(verticalCommandId):
            return

        redis.delete('currentVerticalCommandId')
        self.controller.stop()

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'STOP'

    def needSkip(self, verticalCommandId: str) -> bool:
        if verticalCommandId is not None:
            currentVerticalCommandId = redis.get('currentVerticalCommandId')

            if currentVerticalCommandId is None:
                return True

            currentVerticalCommandId: str = str(currentVerticalCommandId.decode('utf-8'))

            if verticalCommandId != currentVerticalCommandId:
                return True

        return False

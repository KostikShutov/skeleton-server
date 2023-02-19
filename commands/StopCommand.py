import uuid
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface
from utils.Redis import redis


class StopCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, commandId: uuid.UUID, payload: dict) -> bool:
        relatedCommandId: str = payload['relatedCommandId'] if 'relatedCommandId' in payload else None

        if self.needSkip(relatedCommandId):
            return True

        self.controller.stop()

        if relatedCommandId is not None:
            redis.set(
                name='command_' + relatedCommandId,
                value=1,
                ex=300,
            )

        return True

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'STOP'

    def needSkip(self, relatedCommandId: str) -> bool:
        if relatedCommandId is None:
            return False

        currentVerticalCommandId: str = str(redis.get('currentVerticalCommandId').decode('utf-8'))

        return relatedCommandId != currentVerticalCommandId

import uuid
import json
from utils.Redis import redis


class CommandPusher:
    def pushCommand(self, payload: object) -> uuid.UUID:
        from commands.tasks import commandExecute
        commandId: uuid.UUID = self.__generateCommandId()
        body: str = json.dumps(payload)
        commandExecute.delay(commandId=commandId, body=body)
        return commandId

    def __generateCommandId(self) -> uuid.UUID:
        commandId: uuid.UUID = uuid.uuid4()
        redis.set('command_' + str(commandId), 0)
        return commandId

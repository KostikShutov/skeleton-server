import uuid
import json
from utils.Redis import redis


class CommandPusher:
    def pushCommand(self, payload: object) -> uuid.UUID:
        from commands.tasks import commandExecute
        commandId: uuid.UUID = self.generateCommandId()
        body: str = json.dumps(payload)
        commandExecute.delay(commandId=commandId, body=body)
        return commandId

    def pushDelayedCommand(self, payload: object, countdown: int) -> uuid.UUID:
        from commands.tasks import commandDelayedExecute
        commandId: uuid.UUID = self.generateCommandId()
        body: str = json.dumps(payload)
        commandDelayedExecute.s(commandId=commandId, body=body).apply_async(countdown=countdown)
        return commandId

    def pushDelayedStop(self, relatedCommandId: uuid.UUID, duration: int) -> uuid.UUID:
        return self.pushDelayedCommand(
            {
                'name': 'STOP',
                'relatedCommandId': relatedCommandId,
            },
            duration,
        )

    def generateCommandId(self) -> uuid.UUID:
        commandId: uuid.UUID = uuid.uuid4()
        redis.set('command_' + str(commandId), 0)
        return commandId

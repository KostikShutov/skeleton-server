import uuid
import json
from utils.Redis import redis


class CommandPusher:
    def __init__(self):
        self.redis = redis

    def pushCommand(self, payload: object) -> None:
        from commands.tasks import commandExecute
        body: str = json.dumps(payload)
        commandExecute.delay(body)

    def pushDelayedCommand(self, payload: object, countdown: int) -> None:
        from commands.tasks import commandDelayedExecute
        body: str = json.dumps(payload)
        commandDelayedExecute.s(body).apply_async(countdown=countdown)

    def pushDelayedStop(self, duration: int) -> None:
        currentVerticalCommandId: str = str(uuid.uuid4())

        self.redis.set('currentVerticalCommandId', currentVerticalCommandId)

        self.pushDelayedCommand(
            {
                'name': 'STOP',
                'verticalCommandId': currentVerticalCommandId,
            },
            duration,
        )

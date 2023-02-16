import json
from commands.tasks import commandExecute


class CommandPusher:
    def pushCommand(self, payload: object) -> None:
        body: str = json.dumps(payload)
        commandExecute.delay(body)

import uuid


class CommandInterface:
    def execute(self, commandId: uuid.UUID, payload: dict) -> bool:
        pass

    def canExecute(self, payload: dict) -> bool:
        pass

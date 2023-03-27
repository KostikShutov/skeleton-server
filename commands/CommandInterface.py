import uuid


class CommandInterface:
    def execute(self, commandId: uuid.UUID, payload: dict) -> None:
        pass

    def canExecute(self, payload: dict) -> bool:
        pass

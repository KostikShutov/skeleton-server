class CommandInterface:
    def execute(self, payload: dict) -> None:
        pass

    def canExecute(self, payload: dict) -> bool:
        pass

class CommandInterface:
    def execute(self, payload: object) -> None:
        pass

    def canExecute(self, payload: object) -> bool:
        pass

import commands.CommandInterface as CommandInterface
import controllers.ControllerResolver as ControllerResolver


class StopCommand(CommandInterface.CommandInterface):
    def __init__(self):
        self.controller = ControllerResolver.ControllerResolver()

    def execute(self, payload: object) -> None:
        self.controller.resolve().stop()

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'STOP'

import commands.CommandInterface as CommandInterface
import controllers.ControllerResolver as ControllerResolver


class BackwardCommand(CommandInterface.CommandInterface):
    def __init__(self):
        self.controller = ControllerResolver.ControllerResolver()

    def execute(self, payload: object) -> None:
        self.controller.resolve().backward(int(payload['speed']))

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'BACKWARD'

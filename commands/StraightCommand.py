import uuid
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class StraightCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, commandId: uuid.UUID, payload: dict) -> bool:
        self.controller.straight()
        return True

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'STRAIGHT'

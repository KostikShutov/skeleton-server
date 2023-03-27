import uuid
from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class CameraUpCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, commandId: uuid.UUID, payload: dict) -> None:
        self.controller.cameraUp()

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'CAMERA_UP'

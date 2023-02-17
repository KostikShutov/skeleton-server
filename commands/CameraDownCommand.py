from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class CameraDownCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        self.controller.cameraDown()

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'CAMERA_DOWN'

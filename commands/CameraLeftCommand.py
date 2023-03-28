from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class CameraLeftCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        self.controller.cameraLeft()

    def canExecute(self, payload: dict) -> bool:
        return payload['name'] == 'CAMERA_LEFT'

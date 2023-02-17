from commands.CommandInterface import CommandInterface
from controllers.ControllerInterface import ControllerInterface


class CameraRightCommand(CommandInterface):
    def __init__(self, controller: ControllerInterface) -> None:
        self.controller = controller

    def execute(self, payload: dict) -> None:
        self.controller.cameraRight()

    def canExecute(self, payload: object) -> bool:
        return payload['name'] == 'CAMERA_RIGHT'

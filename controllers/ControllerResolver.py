from controllers.ControllerInterface import ControllerInterface
from utils.Config import config


class ControllerResolver:
    def __init__(self) -> None:
        self.controller: str = config['CONTROLLER']

    def resolve(self) -> ControllerInterface:
        if self.controller == 'car_remote':
            from controllers.car.RemoteController import RemoteController
            return RemoteController()
        elif self.controller == 'car_stub':
            from controllers.car.StubController import StubController
            return StubController()
        else:
            raise Exception('Unknown controller')

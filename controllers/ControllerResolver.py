import controllers.ControllerInterface as ControllerInterface
from utils.Config import config


class ControllerResolver:
    def __init__(self):
        self.controller = config['CONTROLLER']

    def resolve(self) -> ControllerInterface:
        if self.controller == 'car_remote':
            import controllers.car.RemoteController as RemoteController
            return RemoteController.RemoteController()
        elif self.controller == 'car_stub':
            import controllers.car.StubController as StubController
            return StubController.StubController()
        else:
            raise Exception('Unknown controller')

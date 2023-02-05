import utils.Config as Config
import controllers.ControllerInterface as ControllerInterface


class ControllerResolver:
    def __init__(self):
        config: dict = Config.Config().getConfig()
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

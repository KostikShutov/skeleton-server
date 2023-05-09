import logging
from controllers.car.AngleService import AngleService
from controllers.car.SpeedService import SpeedService
from controllers.ControllerInterface import ControllerInterface


class StubController(ControllerInterface):
    def __init__(self) -> None:
        self.angleService = AngleService()
        self.speedService = SpeedService()

    def init(self) -> None:
        self.angleService.init()
        self.speedService.init()

    def state(self) -> dict:
        return {
            'minAngle': self.angleService.getMinAngle(),
            'maxAngle': self.angleService.getMaxAngle(),
            'currentAngle': self.angleService.getCurrentAngle(),
            'minSpeed': self.speedService.getMinSpeed(),
            'maxSpeed': self.speedService.getMaxSpeed(),
            'currentSpeed': self.speedService.getCurrentSpeed()
        }

    def forward(self, speed: int) -> None:
        logging.info('Forward (speed: %s)' % speed)

    def backward(self, speed: int) -> None:
        logging.info('Backward (speed: %s)' % speed)

    def stop(self) -> None:
        logging.info('Stop')

    def left(self) -> None:
        oldAngle: int = self.angleService.getCurrentAngle()
        self.angleService.setAngle(self.angleService.getMinAngle())
        newAngle: int = self.angleService.getCurrentAngle()
        logging.info('Left (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def straight(self) -> None:
        oldAngle: int = self.angleService.getCurrentAngle()
        self.angleService.setAngle(self.angleService.getInitAngle())
        newAngle: int = self.angleService.getCurrentAngle()
        logging.info('Straight (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def right(self) -> None:
        oldAngle: int = self.angleService.getCurrentAngle()
        self.angleService.setAngle(self.angleService.getMaxAngle())
        newAngle: int = self.angleService.getCurrentAngle()
        logging.info('Right (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def turn(self, angle: int) -> None:
        oldAngle: int = self.angleService.getCurrentAngle()
        self.angleService.setAngle(angle)
        newAngle: int = self.angleService.getCurrentAngle()
        logging.info('Turn (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def cameraLeft(self) -> None:
        logging.info('Camera left')

    def cameraRight(self) -> None:
        logging.info('Camera right')

    def cameraUp(self) -> None:
        logging.info('Camera up')

    def cameraDown(self) -> None:
        logging.info('Camera down')

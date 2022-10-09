from . import AngleService, SpeedService
from .. import ControllerInterface


class StubController(ControllerInterface.ControllerInterface):
    def __init__(self) -> None:
        self.angleService = AngleService.AngleService()
        self.speedService = SpeedService.SpeedService()

    def init(self):
        return {
            'minAngle': self.angleService.getMinAngle(),
            'maxAngle': self.angleService.getMaxAngle(),
            'currentAngle': self.angleService.getCurrentAngle(),
            'minSpeed': self.speedService.getMinSpeed(),
            'maxSpeed': self.speedService.getMaxSpeed(),
            'currentSpeed': self.speedService.getCurrentSpeed()
        }

    def forward(self, speed) -> None:
        print('forward (speed: %s)' % speed)

    def backward(self, speed) -> None:
        print('backward (speed: %s)' % speed)

    def stop(self) -> None:
        print('stop')

    def left(self) -> None:
        oldAngle = self.angleService.getCurrentAngle()
        self.angleService.setAngle(oldAngle - 45)
        newAngle = self.angleService.getCurrentAngle()
        print("left (oldAngle: %s, newAngle: %s)" % (oldAngle, newAngle))

    def straight(self) -> None:
        oldAngle = self.angleService.getCurrentAngle()
        self.angleService.setAngle(90)
        newAngle = self.angleService.getCurrentAngle()
        print('straight (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def right(self) -> None:
        oldAngle = self.angleService.getCurrentAngle()
        self.angleService.setAngle(oldAngle + 45)
        newAngle = self.angleService.getCurrentAngle()
        print('right (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def turn(self, angle) -> None:
        oldAngle = self.angleService.getCurrentAngle()
        self.angleService.setAngle(angle)
        newAngle = self.angleService.getCurrentAngle()
        print('turn (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def angle(self) -> int:
        angle = self.angleService.getCurrentAngle()
        print('angle (currentAngle: %s)' % angle)
        return angle

    def cameraLeft(self) -> None:
        print('cameraLeft')

    def cameraRight(self) -> None:
        print('cameraRight')

    def cameraUp(self) -> None:
        print('cameraUp')

    def cameraDown(self) -> None:
        print('cameraDown')

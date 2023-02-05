import controllers.car.AngleService as AngleService
import controllers.car.SpeedService as SpeedService
import controllers.ControllerInterface as ControllerInterface
import commands.CommandPusher as CommandPusher


class StubController(ControllerInterface.ControllerInterface):
    def __init__(self) -> None:
        self.angleService = AngleService.AngleService()
        self.speedService = SpeedService.SpeedService()
        self.commandPusher = CommandPusher.CommandPusher()

    def init(self):
        return {
            'minAngle': self.angleService.getMinAngle(),
            'maxAngle': self.angleService.getMaxAngle(),
            'currentAngle': self.angleService.getCurrentAngle(),
            'minSpeed': self.speedService.getMinSpeed(),
            'maxSpeed': self.speedService.getMaxSpeed(),
            'currentSpeed': self.speedService.getCurrentSpeed()
        }

    def pushCommand(self, payload: object) -> None:
        self.commandPusher.pushCommand(payload)

    def forward(self, speed: int) -> None:
        print('Forward (speed: %s)' % speed)

    def backward(self, speed: int) -> None:
        print('Backward (speed: %s)' % speed)

    def stop(self) -> None:
        print('Stop')

    def left(self) -> None:
        oldAngle = self.angleService.getCurrentAngle()
        self.angleService.setAngle(oldAngle - 45)
        newAngle = self.angleService.getCurrentAngle()
        print('Left (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def straight(self) -> None:
        oldAngle = self.angleService.getCurrentAngle()
        self.angleService.setAngle(90)
        newAngle = self.angleService.getCurrentAngle()
        print('Straight (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def right(self) -> None:
        oldAngle = self.angleService.getCurrentAngle()
        self.angleService.setAngle(oldAngle + 45)
        newAngle = self.angleService.getCurrentAngle()
        print('Right (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def turn(self, angle) -> None:
        oldAngle = self.angleService.getCurrentAngle()
        self.angleService.setAngle(angle)
        newAngle = self.angleService.getCurrentAngle()
        print('Turn (oldAngle: %s, newAngle: %s)' % (oldAngle, newAngle))

    def angle(self) -> int:
        angle = self.angleService.getCurrentAngle()
        print('Angle (currentAngle: %s)' % angle)
        return angle

    def cameraLeft(self) -> None:
        print('Camera left')

    def cameraRight(self) -> None:
        print('Camera right')

    def cameraUp(self) -> None:
        print('Camera up')

    def cameraDown(self) -> None:
        print('Camera down')

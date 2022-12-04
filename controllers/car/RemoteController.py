import logging
from . import AngleService, SpeedService, FrontWheels, BackWheels, Camera, PCA9685
from .. import ControllerInterface


class RemoteController(ControllerInterface.ControllerInterface):
    def __init__(self) -> None:
        logging.root.setLevel(logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')

        self.angleService = AngleService.AngleService()
        self.speedService = SpeedService.SpeedService()

        self.frontWheels = FrontWheels.FrontWheels(self.angleService)
        self.backWheels = BackWheels.BackWheels(self.speedService)
        self.camera = Camera.Camera()

        self.frontWheels.ready()
        self.backWheels.ready()
        self.camera.ready()

        pwm = PCA9685.PWM(busNumber=1)
        pwm.setup()
        pwm.frequency = 60

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
        self.speedService.setSpeed(speed)
        self.backWheels.speed = self.speedService.getCurrentSpeed()
        self.backWheels.forward()

    def backward(self, speed) -> None:
        self.speedService.setSpeed(speed)
        self.backWheels.speed = self.speedService.getCurrentSpeed()
        self.backWheels.backward()

    def stop(self) -> None:
        self.backWheels.stop()

    def left(self) -> None:
        self.frontWheels.turnLeft()

    def straight(self) -> None:
        self.frontWheels.turnStraight()

    def right(self) -> None:
        self.frontWheels.turnRight()

    def turn(self, angle) -> None:
        self.frontWheels.turn(angle)

    def angle(self) -> int:
        return self.angleService.getCurrentAngle()

    def cameraLeft(self) -> None:
        self.camera.turnLeft(40)

    def cameraRight(self) -> None:
        self.camera.turnRight(40)

    def cameraUp(self) -> None:
        self.camera.turnUp(20)

    def cameraDown(self) -> None:
        self.camera.turnDown(20)

import logging
from . import AngleService, BackWheels, SpeedService, Camera, FileStorage, FrontWheels, PCA9685, Servo, TB6612
from .. import ControllerInterface


class RemoteController(ControllerInterface.ControllerInterface):
    BUS_NUMBER = 1
    ADDRESS = 0x40
    FREQUENCY = 60

    LEFT_MOTOR_DIRECTION_CHANNEL = 17
    RIGHT_MOTOR_DIRECTION_CHANNEL = 27

    FRONT_WHEEL_CHANNEL = 0
    CAMERA_PAN_CHANNEL = 1
    CAMERA_TILT_CHANNEL = 2
    BACK_LEFT_MOTOR_CHANNEL = 4
    BACK_RIGHT_MOTOR_CHANNEL = 5

    def __init__(self) -> None:
        logging.root.setLevel(logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')

        self.fileStorage = FileStorage.FileStorage()
        self.angleService = AngleService.AngleService()
        self.speedService = SpeedService.SpeedService()
        self.pwm = PCA9685.PWM(busNumber=self.BUS_NUMBER, address=self.ADDRESS)

        self.frontWheels = FrontWheels.FrontWheels(
            angleService=self.angleService,
            servo=Servo.Servo(
                pwm=self.pwm,
                channel=self.FRONT_WHEEL_CHANNEL,
                offset=int(self.fileStorage.get('FRONT_TURNING_OFFSET', defaultValue=0)),
            ),
        )

        self.backWheels = BackWheels.BackWheels(
            speedService=self.speedService,
            pwm=self.pwm,
            leftMotor=TB6612.Motor(
                pwm=self.pwm,
                pwmChannel=self.BACK_LEFT_MOTOR_CHANNEL,
                directionChannel=self.LEFT_MOTOR_DIRECTION_CHANNEL,
                offset=bool(int(self.fileStorage.get('BACK_LEFT_MOTOR_OFFSET', defaultValue=1))),
            ),
            rightMotor=TB6612.Motor(
                pwm=self.pwm,
                pwmChannel=self.BACK_RIGHT_MOTOR_CHANNEL,
                directionChannel=self.RIGHT_MOTOR_DIRECTION_CHANNEL,
                offset=bool(int(self.fileStorage.get('BACK_RIGHT_MOTOR_OFFSET', defaultValue=1))),
            ),
        )

        self.camera = Camera.Camera(
            panServo=Servo.Servo(
                pwm=self.pwm,
                channel=self.CAMERA_PAN_CHANNEL,
                offset=int(self.fileStorage.get('CAMERA_PAN_OFFSET', defaultValue=0)),
            ),
            tiltServo=Servo.Servo(
                pwm=self.pwm,
                channel=self.CAMERA_TILT_CHANNEL,
                offset=int(self.fileStorage.get('CAMERA_TILT_OFFSET', defaultValue=0)),
            ),
        )

        self.frontWheels.ready()
        self.backWheels.ready()
        self.camera.ready()
        self.pwm.setup()

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

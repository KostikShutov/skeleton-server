import logging
from . import FileStorage, Servo, AngleService


class FrontWheels(object):
    FRONT_WHEEL_CHANNEL = 0

    def __init__(self,
                 angleService: AngleService,
                 busNumber: int = 1,
                 channel: int = FRONT_WHEEL_CHANNEL) -> None:
        self.fileStorage = FileStorage.FileStorage()
        self.angleService = angleService

        self.channel = channel
        self.turningOffset = int(self.fileStorage.get('TURNING_OFFSET', defaultValue=0))
        self.servo = Servo.Servo(self.channel, busNumber=busNumber, offset=self.turningOffset)

        logging.info('[Front wheels] Min angle: %s', self.angleService.getMinAngle())
        logging.info('[Front wheels] Max angle: %s', self.angleService.getMaxAngle())
        logging.info('[Front wheels] PWM channel: %s', self.channel)
        logging.info('[Front wheels] Offset value: %s', self.turningOffset)

    def turnLeft(self) -> None:
        self.angleService.setAngle(self.angleService.getMinAngle())
        self.turn(self.angleService.getCurrentAngle())
        logging.info('[Front wheels] Turn left')

    def turnStraight(self) -> None:
        self.angleService.setAngle(90)
        self.turn(self.angleService.getCurrentAngle())
        logging.info('[Front wheels] Turn straight')

    def turnRight(self) -> None:
        self.angleService.setAngle(self.angleService.getMaxAngle())
        self.turn(self.angleService.getCurrentAngle())
        logging.info('[Front wheels] Turn right')

    def turn(self, angle: int) -> None:
        self.angleService.setAngle(angle)
        self.servo.write(self.angleService.getCurrentAngle())
        logging.info('[Front wheels] Turn angle to %s', self.angleService.getCurrentAngle())

    def ready(self) -> None:
        self.servo.offset = self.turningOffset
        self.turnStraight()
        logging.info('[Front wheels] Turn to ready position')

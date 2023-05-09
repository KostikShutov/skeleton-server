import logging
import controllers.car.Servo as Servo
import controllers.car.AngleService as AngleService


class FrontWheels(object):
    def __init__(self,
                 angleService: AngleService,
                 servo: Servo) -> None:
        self.angleService = angleService
        self.servo = servo

        logging.info('[Front wheels] Min angle: %d', self.angleService.getMinAngle())
        logging.info('[Front wheels] Max angle: %d', self.angleService.getMaxAngle())
        logging.info('[Front wheels] Servo PWM channel: %d', self.servo.pwmChannel)
        logging.info('[Front wheels] Servo offset: %d', self.servo.offset)

    def turnLeft(self) -> None:
        self.angleService.setAngle(self.angleService.getMinAngle())
        self.turn(self.angleService.getCurrentAngle(withCast=True))
        logging.info('[Front wheels] Turn left')

    def turnStraight(self) -> None:
        self.angleService.setAngle(self.angleService.getInitAngle())
        self.turn(self.angleService.getCurrentAngle(withCast=True))
        logging.info('[Front wheels] Turn straight')

    def turnRight(self) -> None:
        self.angleService.setAngle(self.angleService.getMaxAngle())
        self.turn(self.angleService.getCurrentAngle(withCast=True))
        logging.info('[Front wheels] Turn right')

    def turn(self, angle: int) -> None:
        self.angleService.setAngle(angle)
        self.servo.write(self.angleService.getCurrentAngle(withCast=True))
        logging.info('[Front wheels] Turn angle to %d', self.angleService.getCurrentAngle())

    def ready(self) -> None:
        self.turnStraight()
        logging.info('[Front wheels] Turn to ready position')

import logging
from . import FileStorage, PCA9685, TB6612, SpeedService


class BackWheels(object):
    MOTOR_A = 17
    MOTOR_B = 27

    PWM_A = 4
    PWM_B = 5

    def __init__(self, speedService: SpeedService, busNumber: int = 1) -> None:
        self.fileStorage = FileStorage.FileStorage()
        self.speedService = speedService

        self.forwardA = bool(int(self.fileStorage.get('FORWARD_A', defaultValue=1)))
        self.forwardB = bool(int(self.fileStorage.get('FORWARD_B', defaultValue=1)))

        self.leftMotor = TB6612.Motor(self.MOTOR_A, offset=self.forwardA)
        self.rightMotor = TB6612.Motor(self.MOTOR_B, offset=self.forwardB)

        self.pwm = PCA9685.PWM(busNumber=busNumber)

        def _set_a_pwm(value) -> None:
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_A, 0, pulse_wide)

        def _set_b_pwm(value) -> None:
            pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
            self.pwm.write(self.PWM_B, 0, pulse_wide)

        self.leftMotor.pwm = _set_a_pwm
        self.rightMotor.pwm = _set_b_pwm

        logging.info('[Back wheels] Min speed: %s', self.speedService.getMinSpeed())
        logging.info('[Back wheels] Max speed: %s', self.speedService.getMaxSpeed())
        logging.info('[Back wheels] Forward A: %s, Forward B: %s', self.forwardA, self.forwardB)
        logging.info('[Back wheels] Set left wheel to %d, PWM channel to %d', self.MOTOR_A, self.PWM_A)
        logging.info('[Back wheels] Set right wheel to %d, PWM channel to %d', self.MOTOR_B, self.PWM_B)

    def forward(self) -> None:
        self.leftMotor.speed = self.speedService.getCurrentSpeed()
        self.rightMotor.speed = self.speedService.getCurrentSpeed()
        self.leftMotor.forward()
        self.rightMotor.forward()
        logging.info('[Back wheels] Running forward with speed %s', self.speedService.getCurrentSpeed())

    def backward(self) -> None:
        self.leftMotor.speed = self.speedService.getCurrentSpeed()
        self.rightMotor.speed = self.speedService.getCurrentSpeed()
        self.leftMotor.backward()
        self.rightMotor.backward()
        logging.info('[Back wheels] Running backward with speed %s' % self.speedService.getCurrentSpeed())

    def stop(self) -> None:
        self.leftMotor.stop()
        self.rightMotor.stop()
        logging.info('[Back wheels] Stop')

    def ready(self) -> None:
        self.leftMotor.offset = self.forwardA
        self.rightMotor.offset = self.forwardB
        self.stop()
        logging.info('[Back wheels] Turn to ready position')

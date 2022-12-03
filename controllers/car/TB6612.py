import logging
import RPi.GPIO as GPIO


class Motor(object):
    def __init__(self, directionChannel: int, pwm=None, offset: bool = True) -> None:
        self.directionChannel = directionChannel
        self._pwm = pwm
        self._offset = offset
        self.forwardOffset = self._offset
        self.backwardOffset = not self.forwardOffset
        self._speed = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.directionChannel, GPIO.OUT)

        logging.info('[Motor] Setup motor direction channel at %s', self.directionChannel)
        logging.info('[Motor] Setup motor pwm channel')
        # logging.info('[Motor] Setup motor pwm channel as %s', self._pwm.__name__)

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, speed) -> None:
        if speed not in range(0, 101):
            raise ValueError('Speed ranges from 0 to 100, not "{0}"'.format(speed))
        if not callable(self._pwm):
            raise ValueError(
                'pwm is not callable, please set Motor.pwm to a pwm control function with only 1 variable speed')
        logging.info('[Motor] Set speed to %s', speed)
        self._speed = speed
        self._pwm(self._speed)

    def forward(self) -> None:
        GPIO.output(self.directionChannel, self.forwardOffset)
        self.speed = self._speed
        logging.info('[Motor] Moving forward (%s)', str(self.forwardOffset))

    def backward(self) -> None:
        GPIO.output(self.directionChannel, self.backwardOffset)
        self.speed = self._speed
        logging.info('[Motor] Moving backward (%s)', str(self.backwardOffset))

    def stop(self) -> None:
        self.speed = 0
        logging.info('[Motor] Stop')

    @property
    def offset(self) -> bool:
        return self._offset

    @offset.setter
    def offset(self, value: bool) -> None:
        self.forwardOffset = value
        self.backwardOffset = not self.forwardOffset
        logging.info('[Motor] Set offset to %d', self._offset)

    @property
    def pwm(self):
        return self._pwm

    @pwm.setter
    def pwm(self, pwm) -> None:
        self._pwm = pwm
        logging.info('[Motor] Set pwm')

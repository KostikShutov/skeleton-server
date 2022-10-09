import logging
from . import PCA9685


class Servo(object):
    MIN_PULSE_WIDTH = 600
    MAX_PULSE_WIDTH = 2400
    DEFAULT_PULSE_WIDTH = 1500
    FREQUENCY = 60

    def __init__(self, channel: int, offset: int = 0, lock: bool = True, busNumber: int = 1, address=0x40) -> None:
        if channel < 0 or channel > 16:
            raise ValueError("Servo channel \"{0}\" is not in (0, 15).".format(channel))
        self.channel = channel
        self.offset = offset
        self.lock = lock

        self.pwm = PCA9685.PWM(busNumber=busNumber, address=address)
        self.frequency = self.FREQUENCY
        self.write(90)

    def setup(self) -> None:
        self.pwm.setup()

    def _angle_to_analog(self, angle) -> int:
        """ Calculate 12-bit analog value from giving angle """
        pulseWide = self.pwm.map(angle, 0, 180, self.MIN_PULSE_WIDTH, self.MAX_PULSE_WIDTH)
        analogValue = int(float(pulseWide) / 1000000 * self.frequency * 4096)
        logging.info('[Servo] Angle %d equals analogValue %d', angle, analogValue)
        return analogValue

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value
        self.pwm.frequency = value

    @property
    def offset(self) -> int:
        return self._offset

    @offset.setter
    def offset(self, value: int) -> None:
        """ Set offset for much user-friendly """
        self._offset = value
        logging.info('[Servo] Set offset to %d', self.offset)

    def write(self, angle: int) -> None:
        """ Turn the servo with giving angle. """
        if self.lock:
            if angle > 180:
                angle = 180
            if angle < 0:
                angle = 0
        else:
            if angle < 0 or angle > 180:
                raise ValueError("Servo \"{0}\" turn angle \"{1}\" is not in (0, 180).".format(self.channel, angle))
        val = self._angle_to_analog(angle)
        val += self.offset
        self.pwm.write(self.channel, 0, val)
        logging.info('[Servo] Turn angle = %d', angle)

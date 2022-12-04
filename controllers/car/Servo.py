import logging
from . import PCA9685


class Servo(object):
    MIN_PULSE_WIDTH = 600
    MAX_PULSE_WIDTH = 2400
    DEFAULT_PULSE_WIDTH = 1500

    def __init__(self,
                 pwm: PCA9685,
                 channel: int,
                 offset: int = 0,
                 ) -> None:
        if channel < 0 or channel > 16:
            raise ValueError("Servo channel \"{0}\" is not in (0, 15).".format(channel))

        self.pwm = pwm
        self.channel = channel
        self.offset = offset

        self.write(90)

    def angleToAnalog(self, angle) -> int:
        """ Calculate 12-bit analog value from giving angle """
        pulseWide = self.pwm.map(angle, 0, 180, self.MIN_PULSE_WIDTH, self.MAX_PULSE_WIDTH)
        analogValue = int(float(pulseWide) / 1000000 * self.pwm.frequency * 4096)
        logging.info('[Servo] Angle: %d, Analog value: %d', angle, analogValue)
        return analogValue

    def write(self, angle: int) -> None:
        """ Turn the servo with giving angle. """
        if angle > 180:
            angle = 180
        if angle < 0:
            angle = 0

        val = self.angleToAnalog(angle)
        val += self.offset
        self.pwm.write(self.channel, 0, val)
        logging.info('[Servo] Turn angle to %d', angle)

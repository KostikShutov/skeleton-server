import logging
from . import FileStorage, Servo


class Camera(object):
    PAN_CHANNEL = 1  # Pan servo channel
    TILT_CHANNEL = 2  # Tilt servo channel

    READY_PAN = 90  # Ready position angle
    READY_TILT = 90  # Ready position angle
    CALI_PAN = 90  # Calibration position angle
    CALI_TILT = 90  # Calibration position angle

    CAMERA_DELAY = 0.005
    PAN_STEP = 15  # Pan step = 5 degree
    TILT_STEP = 10  # Tilt step = 5 degree

    def __init__(self, busNumber: int = 1) -> None:
        self.fileStorage = FileStorage.FileStorage()
        self.panOffset = int(self.fileStorage.get('PAN_OFFSET', defaultValue=0))
        self.tiltOffset = int(self.fileStorage.get('TILT_OFFSET', defaultValue=0))

        self.panServo = Servo.Servo(self.PAN_CHANNEL, busNumber=busNumber, offset=self.panOffset)
        self.tiltServo = Servo.Servo(self.TILT_CHANNEL, busNumber=busNumber, offset=self.tiltOffset)

        self.currentPan = 0
        self.currentTilt = 0

        logging.info('[Camera] Pan servo channel: %d', self.PAN_CHANNEL)
        logging.info('[Camera] Tilt servo channel: %d', self.TILT_CHANNEL)
        logging.info('[Camera] Pan offset value: %d', self.panOffset)
        logging.info('[Camera] Tilt offset value: %d', self.tiltOffset)

    def safePlus(self, variable: int, plusValue: int) -> int:
        variable += plusValue
        if variable > 180:
            variable = 180
        if variable < 0:
            variable = 0
        return variable

    def turnLeft(self, step: int = PAN_STEP) -> None:
        self.currentPan = self.safePlus(self.currentPan, step)
        self.panServo.write(self.currentPan)
        logging.info('[Camera] Turn left at step: %d', step)

    def turnRight(self, step: int = PAN_STEP) -> None:
        self.currentPan = self.safePlus(self.currentPan, -step)
        self.panServo.write(self.currentPan)
        logging.info('[Camera] Turn right at step: %d', step)

    def turnUp(self, step: int = TILT_STEP) -> None:
        self.currentTilt = self.safePlus(self.currentTilt, step)
        self.tiltServo.write(self.currentTilt)
        logging.info('[Camera] Turn up at step: %d', step)

    def turnDown(self, step: int = TILT_STEP) -> None:
        self.currentTilt = self.safePlus(self.currentTilt, -step)
        self.tiltServo.write(self.currentTilt)
        logging.info('[Camera] Turn down at step: %d', step)

    def ready(self) -> None:
        self.panServo.offset = self.panOffset
        self.tiltServo.offset = self.tiltOffset
        self.currentPan = self.READY_PAN
        self.currentTilt = self.READY_TILT
        self.panServo.write(self.currentPan)
        self.tiltServo.write(self.currentTilt)
        logging.info('[Camera] Turn to ready position')

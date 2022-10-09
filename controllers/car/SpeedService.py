class SpeedService:
    def __init__(self, minSpeed: int = 1, maxSpeed: int = 100) -> None:
        self.currentSpeed = None
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.setSpeed(60)

    def getCurrentSpeed(self) -> int:
        return self.currentSpeed

    def getMinSpeed(self) -> int:
        return self.minSpeed

    def getMaxSpeed(self) -> int:
        return self.maxSpeed

    def setSpeed(self, speed: int) -> None:
        if speed < self.minSpeed:
            self.currentSpeed = self.minSpeed
        elif speed > self.maxSpeed:
            self.currentSpeed = self.maxSpeed
        else:
            self.currentSpeed = speed

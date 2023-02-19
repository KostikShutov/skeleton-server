from utils.Redis import redis


class SpeedService:
    def __init__(self, minSpeed: int = 1, maxSpeed: int = 100) -> None:
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed

    def init(self) -> None:
        self.setSpeed(60)

    def getCurrentSpeed(self) -> int:
        return int(redis.get('currentSpeed').decode('utf-8'))

    def getMinSpeed(self) -> int:
        return self.minSpeed

    def getMaxSpeed(self) -> int:
        return self.maxSpeed

    def setSpeed(self, speed: int) -> None:
        if speed < self.minSpeed:
            redis.set('currentSpeed', self.minSpeed)
        elif speed > self.maxSpeed:
            redis.set('currentSpeed', self.maxSpeed)
        else:
            redis.set('currentSpeed', speed)

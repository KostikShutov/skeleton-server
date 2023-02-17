from utils.Redis import redis


class AngleService:
    def __init__(self, minAngle: int = 45, maxAngle: int = 135) -> None:
        self.minAngle: int = minAngle
        self.maxAngle: int = maxAngle
        self.setAngle(90)

    def getCurrentAngle(self) -> int:
        return int(redis.get('currentAngle').decode('utf-8'))

    def getMinAngle(self) -> int:
        return self.minAngle

    def getMaxAngle(self) -> int:
        return self.maxAngle

    def setAngle(self, angle: int) -> None:
        if angle < self.minAngle:
            redis.set('currentAngle', self.minAngle)
        elif angle > self.maxAngle:
            redis.set('currentAngle', self.maxAngle)
        else:
            redis.set('currentAngle', angle)

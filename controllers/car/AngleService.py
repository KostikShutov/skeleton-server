from utils.Redis import redis


class AngleService:
    def __init__(self, minAngle: int = 45, maxAngle: int = 135) -> None:
        self.redis = redis
        self.minAngle: int = minAngle
        self.maxAngle: int = maxAngle

    def getCurrentAngle(self) -> int:
        return int(self.redis.get('currentAngle').decode('utf-8'))

    def getMinAngle(self) -> int:
        return self.minAngle

    def getMaxAngle(self) -> int:
        return self.maxAngle

    def setAngle(self, angle: int) -> None:
        if angle < self.minAngle:
            self.redis.set('currentAngle', self.minAngle)
        elif angle > self.maxAngle:
            self.redis.set('currentAngle', self.maxAngle)
        else:
            self.redis.set('currentAngle', angle)

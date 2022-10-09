class AngleService:
    def __init__(self, minAngle: int = 45, maxAngle: int = 135) -> None:
        self.currentAngle = None
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.setAngle(90)

    def getCurrentAngle(self) -> int:
        return self.currentAngle

    def getMinAngle(self) -> int:
        return self.minAngle

    def getMaxAngle(self) -> int:
        return self.maxAngle

    def setAngle(self, angle: int) -> None:
        if angle < self.minAngle:
            self.currentAngle = self.minAngle
        elif angle > self.maxAngle:
            self.currentAngle = self.maxAngle
        else:
            self.currentAngle = angle

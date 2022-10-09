class ControllerInterface:
    def init(self):
        pass

    def forward(self, speed) -> None:
        pass

    def backward(self, speed) -> None:
        pass

    def stop(self) -> None:
        pass

    def left(self) -> None:
        pass

    def straight(self) -> None:
        pass

    def right(self) -> None:
        pass

    def turn(self, angle) -> None:
        pass

    def angle(self) -> int:
        pass

    def cameraLeft(self) -> None:
        pass

    def cameraRight(self) -> None:
        pass

    def cameraUp(self) -> None:
        pass

    def cameraDown(self) -> None:
        pass

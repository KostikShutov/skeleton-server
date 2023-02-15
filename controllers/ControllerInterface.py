class ControllerInterface:
    def init(self):
        pass

    def pushCommand(self, payload: object) -> None:
        pass

    def forward(self, speed: int, distance: int = None, duration: int = None) -> None:
        pass

    def backward(self, speed: int, distance: int = None, duration: int = None) -> None:
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

import time


def microSleep(duration: float) -> None:
    timer = time.time()

    while timer + duration > time.time():
        pass

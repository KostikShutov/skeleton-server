import gpsd


class Gps:
    def __init__(self) -> None:
        gpsd.connect(host='localhost')

    def getLatitude(self) -> float:
        return gpsd.get_current().lat

    def getLongitude(self) -> float:
        return gpsd.get_current().lon

from abc import ABC
from geometry.point import Point


class Locatable(ABC):
    def get_x(self) -> float:
        raise NotImplementedError()

    def get_y(self) -> float:
        raise NotImplementedError()

    def to_point(self) -> Point:
        return Point(self.get_x(), self.get_y())

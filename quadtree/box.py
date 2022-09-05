from typing import Union
from dataclasses import dataclass
from quadtree.point import Point
from quadtree.locatable import Locatable


@dataclass
class Box:
    top_left: Point
    bottom_right: Point

    @property
    def left(self) -> float:
        return self.top_left.x

    @property
    def right(self) -> float:
        return self.bottom_right.x

    @property
    def top(self) -> float:
        return self.top_left.y

    @property
    def bottom(self) -> float:
        return self.bottom_right.y

    def copy(self) -> 'Box':
        return Box(self.top_left.copy(), self.bottom_right.copy())

    def contains(self, item: Union[Point, Locatable]) -> bool:
        x, y = Point.xy(item)
        return self.top_left.x <= x <= self.bottom_right.x and self.top_left.y <= y <= self.bottom_right.y

    def overlap(self, box: 'Box') -> bool:
        return self._overlap(
            self.left, self.right, box.left, box.right) and self._overlap(
            self.top, self.bottom, box.top, box.bottom)

    def _overlap(self, x1: float, y1: float, x2: float, y2: float) -> bool:
        return x1 <= y2 and y1 >= x2

    @classmethod
    def create(cls, x1: float, y1: float, x2: float, y2: float) -> 'Box':
        return Box(Point(x1, y1), Point(x2, y2))

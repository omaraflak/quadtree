from typing import Union
from dataclasses import dataclass
from quadtree.locatable import Locatable


@dataclass
class Point:
    x: float
    y: float

    def copy(self) -> 'Point':
        return Point(self.x, self.y)

    def distance_to(self, item: Union['Point', Locatable]) -> float:
        x, y = Point.xy(item)
        return ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5

    @staticmethod
    def xy(item: Union['Point', Locatable]) -> tuple[float, float]:
        if isinstance(item, Point):
            return item.x, item.y
        return item.get_x(), item.get_y()

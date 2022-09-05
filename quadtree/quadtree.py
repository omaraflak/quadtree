from typing import Optional, Generic, TypeVar, Callable
from dataclasses import dataclass, field
from quadtree.locatable import Locatable
from quadtree.point import Point
from quadtree.box import Box


T = TypeVar('T', bound=Locatable)


@dataclass
class QuadTree(Generic[T]):
    MAX_CAPACITY = 20

    box: Box
    data: set[T] = field(default_factory=set)
    top_left_node: Optional['QuadTree'] = None
    top_right_node: Optional['QuadTree'] = None
    bottom_right_node: Optional['QuadTree'] = None
    bottom_left_node: Optional['QuadTree'] = None
    is_split: bool = False

    def add(self, item: T):
        if len(self.data) == QuadTree.MAX_CAPACITY:
            self._split()

        self._add(item)

    def remove(self, item: T):
        if not self.box.contains(item):
            return

        if not self.is_split:
            if item in self.data:
                self.data.remove(item)
            return

        if self.top_left_node.box.contains(item):
            self.top_left_node.remove(item)
        if self.top_right_node.box.contains(item):
            self.top_right_node.remove(item)
        if self.bottom_right_node.box.contains(item):
            self.bottom_right_node.remove(item)
        if self.bottom_left_node.box.contains(item):
            self.bottom_left_node.remove(item)

    def get(self, box: Box) -> set[T]:
        if not self.box.overlap(box):
            return set()

        if not self.is_split:
            return self._get(box)

        result = set()
        if self.top_left_node.box.overlap(box):
            result |= self.top_left_node._get(box)
        if self.top_right_node.box.overlap(box):
            result |= self.top_right_node._get(box)
        if self.bottom_right_node.box.overlap(box):
            result |= self.bottom_right_node._get(box)
        if self.bottom_left_node.box.overlap(box):
            result |= self.bottom_left_node._get(box)

        return result

    def get_in_circle(self, center: Point, radius: float) -> set[T]:
        box = Box(
            Point(center.x - radius, center.y - radius),
            Point(center.x + radius, center.y + radius)
        )
        return {
            item
            for item in self.get(box)
            if center.distance_to(item) <= radius
        }

    def all(self) -> set[T]:
        if not self.is_split:
            return self.data

        result = set()
        result |= self.top_left_node.all()
        result |= self.top_right_node.all()
        result |= self.bottom_right_node.all()
        result |= self.bottom_left_node.all()
        return result

    def copy(self, copy_item: Callable[[T], T]) -> 'QuadTree[T]':
        return QuadTree(
            self.box.copy(),
            {copy_item(item) for item in self.data},
            self.top_left_node.copy(copy_item) if self.top_left_node else None,
            self.top_right_node.copy(copy_item) if self.top_right_node else None,
            self.bottom_right_node.copy(copy_item) if self.bottom_right_node else None,
            self.bottom_left_node.copy(copy_item) if self.bottom_left_node else None,
            self.is_split
        )

    def _split(self):
        top = self.box.top
        right = self.box.right
        bottom = self.box.bottom
        left = self.box.left

        middle_x = (left + right) / 2
        middle_y = (top + bottom) / 2

        self.top_left_node = QuadTree(Box(self.box.top_left, Point(middle_x, middle_y)))
        self.top_right_node = QuadTree(Box(Point(middle_x, top), Point(right, middle_y)))
        self.bottom_right_node = QuadTree(Box(Point(middle_x, middle_y), self.box.bottom_right))
        self.bottom_left_node = QuadTree(Box(Point(left, middle_y), Point(middle_x, bottom)))
        self.is_split = True

        for item in self.data:
            self._add(item)

        self.data.clear()

    def _add(self, item: T):
        if not self.is_split:
            self.data.add(item)
            return

        if self.top_left_node.box.contains(item):
            self.top_left_node.data.add(item)
        elif self.top_right_node.box.contains(item):
            self.top_right_node.data.add(item)
        elif self.bottom_right_node.box.contains(item):
            self.bottom_right_node.data.add(item)
        else:
            self.bottom_left_node.data.add(item)

    def _get(self, box: Box) -> set[T]:
        return {item for item in self.data if box.contains(item)}

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
    items: list[T] = field(default_factory=list)
    top_left_node: Optional['QuadTree'] = None
    top_right_node: Optional['QuadTree'] = None
    bottom_right_node: Optional['QuadTree'] = None
    bottom_left_node: Optional['QuadTree'] = None

    @property
    def is_split(self) -> bool:
        return self.top_left_node is not None

    def add(self, item: T):
        if not self.box.contains(item):
            return

        if len(self.items) == QuadTree.MAX_CAPACITY:
            self._split()

        self._add(item)

    def remove(self, item: T):
        if not self.box.contains(item):
            return

        if not self.is_split:
            if item in self.items:
                self.items.remove(item)
            return

        self.top_left_node.remove(item)
        self.top_right_node.remove(item)
        self.bottom_right_node.remove(item)
        self.bottom_left_node.remove(item)

    def get(self, box: Box) -> list[T]:
        if not self.box.overlap(box):
            return []

        if not self.is_split:
            return self._get(box)

        return [
            *self.top_left_node._get(box),
            *self.top_right_node._get(box),
            *self.bottom_right_node._get(box),
            *self.bottom_left_node._get(box)
        ]

    def get_in_circle(self, center: Point, radius: float) -> set[T]:
        box = Box.create(
            center.x - radius,
            center.y - radius,
            center.x + radius,
            center.y + radius
        )
        return {
            item
            for item in self.get(box)
            if center.distance_to(item) <= radius
        }

    def all(self) -> list[T]:
        if not self.is_split:
            return self.items

        result = list()
        result.extend(self.top_left_node.all())
        result.extend(self.top_right_node.all())
        result.extend(self.bottom_right_node.all())
        result.extend(self.bottom_left_node.all())
        return result

    def copy(self, copy_item: Callable[[T], T]) -> 'QuadTree[T]':
        return QuadTree(
            self.box.copy(),
            [copy_item(item) for item in self.items],
            self.top_left_node.copy(copy_item) if self.top_left_node else None,
            self.top_right_node.copy(copy_item) if self.top_right_node else None,
            self.bottom_right_node.copy(copy_item) if self.bottom_right_node else None,
            self.bottom_left_node.copy(copy_item) if self.bottom_left_node else None
        )

    def _split(self):
        top = self.box.top
        right = self.box.right
        bottom = self.box.bottom
        left = self.box.left

        middle_x = (left + right) / 2
        middle_y = (top + bottom) / 2

        self.top_left_node = QuadTree(Box.create(left, top, middle_x, middle_y))
        self.top_right_node = QuadTree(Box.create(middle_x, top, right, middle_y))
        self.bottom_right_node = QuadTree(Box.create(middle_x, middle_y, right, bottom))
        self.bottom_left_node = QuadTree(Box.create(left, middle_y, middle_x, bottom))

        for item in self.items:
            self._add(item)

        self.items.clear()

    def _add(self, item: T):
        if not self.is_split:
            self.items.append(item)
            return

        if self.top_left_node.box.contains(item):
            self.top_left_node.items.append(item)
        elif self.top_right_node.box.contains(item):
            self.top_right_node.items.append(item)
        elif self.bottom_right_node.box.contains(item):
            self.bottom_right_node.items.append(item)
        elif self.bottom_left_node.box.contains(item):
            self.bottom_left_node.items.append(item)

    def _get(self, box: Box) -> list[T]:
        return [item for item in self.items if box.contains(item)]

from typing import Optional, Generic, TypeVar, Callable
from dataclasses import dataclass, field
from quadtree.locatable import Locatable
from geometry.point import Point
from geometry.box import Box


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
    split_criteria: Optional[Callable[[list[T]], bool]] = None
    depth: int = 0
    max_depth: int = 0

    @property
    def is_split(self) -> bool:
        return self.top_left_node is not None

    def add(self, item: T):
        if not self.box.contains(item.to_point()):
            return

        if self._should_split(self.items):
            self._split()

        self._add(item)

    def remove(self, item: T):
        if not self.box.contains(item.to_point()):
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
        if not self.box.intersect(box):
            return []

        if not self.is_split:
            return [
                item
                for item in self.items
                if box.contains(item.to_point())
            ]

        return [
            *self.top_left_node.get(box),
            *self.top_right_node.get(box),
            *self.bottom_right_node.get(box),
            *self.bottom_left_node.get(box)
        ]

    def get_in_circle(self, center: Point, radius: float) -> list[T]:
        box = Box.create(
            center.x - radius,
            center.y - radius,
            center.x + radius,
            center.y + radius
        )
        return [
            item
            for item in self.get(box)
            if center.distance_to(item.to_point()) <= radius
        ]

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
            self.bottom_left_node.copy(copy_item) if self.bottom_left_node else None,
            self.split_criteria,
            self.depth,
            self.max_depth,
        )

    def _should_split(self, items: list[T]) -> bool:
        if self.max_depth > 0 and self.depth >= self.max_depth:
            return False

        if not self.split_criteria:
            return len(items) == QuadTree.MAX_CAPACITY

        return self.split_criteria(items)

    def _split(self):
        top = self.box.top
        right = self.box.right
        bottom = self.box.bottom
        left = self.box.left

        middle_x = (left + right) / 2
        middle_y = (top + bottom) / 2

        self.top_left_node = self._next_level_node(Box.create(left, top, middle_x, middle_y))
        self.top_right_node = self._next_level_node(Box.create(middle_x, top, right, middle_y))
        self.bottom_right_node = self._next_level_node(Box.create(middle_x, middle_y, right, bottom))
        self.bottom_left_node = self._next_level_node(Box.create(left, middle_y, middle_x, bottom))

        for item in self.items:
            self._add(item)

        self.items.clear()

    def _next_level_node(self, box: Box) -> 'QuadTree[T]':
        return QuadTree(
            box,
            depth=self.depth + 1,
            max_depth=self.max_depth,
            split_criteria=self.split_criteria
        )

    def _add(self, item: T):
        if not self.is_split:
            self.items.append(item)
            return

        if self.top_left_node.box.contains(item.to_point()):
            self.top_left_node.add(item)
        elif self.top_right_node.box.contains(item.to_point()):
            self.top_right_node.add(item)
        elif self.bottom_right_node.box.contains(item.to_point()):
            self.bottom_right_node.add(item)
        elif self.bottom_left_node.box.contains(item.to_point()):
            self.bottom_left_node.add(item)


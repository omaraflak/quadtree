from dataclasses import dataclass
from quadtree.quadtree import QuadTree
from quadtree.locatable import Locatable
from quadtree.box import Box


@dataclass
class MyObject(Locatable):
    x: float
    y: float

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


QuadTree.MAX_CAPACITY = 2
q: QuadTree[MyObject] = QuadTree(Box.create(0, 0, 100, 100))

q.add(MyObject(1, 1))
q.add(MyObject(2, 2))
q.add(MyObject(5, 5))
q.add(MyObject(90, 90))

# {{(1, 1), (2, 2), (5, 5)}, {(90, 90)}}
print(q)

# {(5, 5), (90, 90)}
print(q.get(Box.create(4, 4, 95, 95)))

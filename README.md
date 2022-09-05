# QuadTree

A QuadTree is a tree data structure where each node is connected to 4 nodes when the number of items added to each node exceeds a certain capacity. The data is split according to the spacial properties of the item (x,y coordinates).

[https://en.wikipedia.org/wiki/Quadtree](https://en.wikipedia.org/wiki/Quadtree)

# Use

```python
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


QuadTree.MAX_CAPACITY = 2
q: QuadTree[MyObject] = QuadTree(Box.create(0, 0, 100, 100))

q.add(MyObject(1, 1))
q.add(MyObject(2, 2))
q.add(MyObject(5, 5))
q.add(MyObject(90, 90))

# {{(1, 1), (2, 2), (5, 5)}, {(90, 90)}}
print(q)

# {(5, 5), (90, 90)}
q.get(Box.create(4, 4, 95, 95))
```
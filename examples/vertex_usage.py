"""Basic usage example for the circular linked list."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.vertex import Vertex
from src.core.point import Point

p1 = Point(1, 2)
v1 = Vertex.from_point(p1)

print("Vertex v1:", v1)
print("Point from v1:", v1.point())

print("Neighbors of v1 (should be itself):", v1.cw(), v1.ccw())

print("Inserting new vertex v2 after v1...")
p2 = Point(3, 4)
v2 = Vertex.from_point(p2)
v1.insert(v2)
print("Neighbors of v1 after insertion:", v1.cw(), v1.ccw())

print("Inserting new vertex v3 after v2...")
p3 = Point(5, 6)
v3 = Vertex.from_point(p3)
v2.insert(v3)
print("Neighbors of v2 after insertion:", v2.cw(), v2.ccw())
print("Neighbors of v3 after insertion:", v3.cw(), v3.ccw())
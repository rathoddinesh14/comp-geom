from __future__ import annotations

from src.core.edge import Edge
from src.core.intersect_enum import Intersection_Type
from src.core.point_enum import Point_Position
from src.core.rotation_enum import Rotation
from .point3d import Point3D
from typing import Tuple, cast
from .edge3d import Edge3D
from .polygon import Polygon
from .vertex import Vertex

class Triangle3D:
    def __init__(self, p1: Point3D, p2: Point3D, p3: Point3D, id: int = 0) -> None:
        self._vertices = [p1, p2, p3]
        self._id = id
        self._bounding_box = self._compute_bounding_box()

    def __repr__(self) -> str:
        return f"Triangle3D({self._vertices[0]}, {self._vertices[1]}, {self._vertices[2]}, id={self._id})"

    def __getitem__(self, index: int) -> Point3D:
        return self._vertices[index]

    def _compute_bounding_box(self):
        min_x = min(p.x for p in self._vertices)
        max_x = max(p.x for p in self._vertices)
        min_y = min(p.y for p in self._vertices)
        max_y = max(p.y for p in self._vertices)
        min_z = min(p.z for p in self._vertices)
        max_z = max(p.z for p in self._vertices)
        return Edge3D(Point3D(min_x, min_y, min_z), Point3D(max_x, max_y, max_z))

    def bounding_box(self) -> Edge3D:
        return self._bounding_box

    def n(self) -> Point3D:
        """Computes the normal vector of the triangle."""
        v1 = self._vertices[1] - self._vertices[0]
        v2 = self._vertices[2] - self._vertices[0]
        c = v1.cross(v2)
        l = c.length()
        if l < 1e-6:
            return Point3D(0, 0, 0)
        return c / l
    
    def project(self, h: int, v: int) -> Polygon:
        """Project a 3D triangle onto a 2D plane defined by indices h and v."""
        p = Polygon(Vertex(self[0][h], self[0][v]))
        p.insert(Vertex(self[1][h], self[1][v]))
        c = Vertex(self[2][h], self[2][v])
        
        if c.classify_edge(cast(Edge, p.edge())) == Point_Position.RIGHT:
            p.advance(Rotation.CW)
        p.insert(c)

        return p

    def lineTriangleIntersect(self, edge: Edge3D) -> Tuple[Intersection_Type, float]:
        """Check if edge intersects triangle and return intersection point if it exists."""
        a_class, t = edge.intersect(self)
        if (a_class in (Intersection_Type.COLLINEAR, Intersection_Type.PARALLEL)):
            return a_class, 0.0
        q = edge.point_at(t)

        h, v = -1, -1
        n = self.n()
        if (n.dot(Point3D(1, 0, 0)) != 0.0):
            h, v = 1, 2
        elif (n.dot(Point3D(0, 0, 1)) != 0.0):
            h, v = 0, 1
        else:
            h, v = 2, 0
        
        poly = self.project(h, v)
        qp = Vertex(q[h], q[v])
        ans = poly.pointInPolygon(qp)
        return (Intersection_Type.SKEW_CROSS if ans else Intersection_Type.SKEW_NO_CROSS, t)
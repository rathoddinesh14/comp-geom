from __future__ import annotations
import math
from typing import Tuple, Optional, TYPE_CHECKING


from src.core.intersect_enum import Intersection_Type
from src.core.edge_enum import Edge_Type

if TYPE_CHECKING:
    from .point import Point


from .point_enum import Point_Position
from .geom_utils import dot

class Edge:
    def __init__(self, org: Optional['Point'] = None, dest: Optional['Point'] = None) -> None:
        from .point import Point
        self.org = org if org else Point()
        self.dest = dest if dest else Point(1, 0)

    # -------------------------
    # Transformations
    # -------------------------

    def rot(self) -> 'Edge':
        """
        Rotate edge 90 degrees clockwise around midpoint.
        """
        from .point import Point
        mid = (self.org + self.dest) / 2
        dir_vec = self.dest - self.org
        n_vec = Point(dir_vec.y, -dir_vec.x)  # Rotate direction vector
        self.org = mid - n_vec * 0.5
        self.dest = mid + n_vec * 0.5
        return self

    def flip(self) -> 'Edge':
        """Reverse the edge direction."""
        original_org = self.org
        self.org = self.dest
        self.dest = original_org
        return self

    # -------------------------
    # Parametric point
    # -------------------------

    def point(self, t: float) -> 'Point':
        """
        Return point along edge:
        t=0 → org
        t=1 → dest
        """
        return self.org + (self.dest - self.org) * t

    # -------------------------
    # Geometry
    # -------------------------

    def is_vertical(self) -> bool:
        return math.isclose(self.org.x, self.dest.x)

    def slope(self) -> float:
        if self.is_vertical():
            return float('inf')
        return (self.dest.y - self.org.y) / (self.dest.x - self.org.x)

    def y(self, x: float) -> float:
        """Compute y for given x on the line."""
        if self.is_vertical():
            raise ValueError("Vertical line has no unique y for given x")

        m = self.slope()
        return self.org.y + m * (x - self.org.x)

    # -------------------------
    # Intersection
    # -------------------------

    def intersect(self, other: 'Edge') -> Tuple[Intersection_Type, Optional[float]]:
        """
        Check intersection (infinite lines).
        Returns (True, t) where t is parameter on self.
        """
        from .point import Point
        a = self.dest - self.org
        b = other.dest - other.org
        c = other.org - self.org
        n = Point(b.y, -b.x)  # Normal to b

        denom = dot(a, n)

        if math.isclose(denom, 0):
            a_class = self.org.classify_edge(other)
            if a_class in (Point_Position.LEFT, Point_Position.RIGHT):
                return Intersection_Type.PARALLEL, None  # Parallel and non-coincident
            return Intersection_Type.COLLINEAR, None  # Coincident

        num = dot(-c, n)
        t = -num / denom
        return Intersection_Type.SKEW, t

    def cross(self, other: 'Edge') -> Tuple[Intersection_Type, Optional[float]]:
        """
        Segment intersection (0 <= t <= 1)
        """
        cross_type, t = other.intersect(self)
        if cross_type in (Intersection_Type.PARALLEL, Intersection_Type.COLLINEAR):
            return cross_type, None
        if t is not None:
            if t < 0 or t > 1:
                return Intersection_Type.SKEW_NO_CROSS, None
            # Check if intersection point is on the other segment
            s = self.intersect(other)[1]
            if s is not None and (s < 0 or s > 1):
                return Intersection_Type.SKEW_NO_CROSS, None
            return Intersection_Type.SKEW_CROSS, s
        return cross_type, t
    
    def edge_type(self, p: 'Point') -> Edge_Type:
        """
        detects edge crossing
        """
        v = self.org
        w = self.dest
        c = p.classify_edge(self)
        match c:
            case Point_Position.LEFT:
                #       \(w) 
                #        \
                #  (p)    \
                #          \(v)
                return Edge_Type.CROSSING if v.y < p.y and p.y <= w.y else Edge_Type.INESSENTIAL
            case Point_Position.RIGHT:
                #       \(v) 
                #        \
                #  (p)    \
                #          \(w)
                return Edge_Type.CROSSING if w.y < p.y and p.y <= v.y else Edge_Type.INESSENTIAL
            case Point_Position.BETWEEN | Point_Position.ORIGIN | Point_Position.DESTINATION:
                return Edge_Type.TOUCHING
            case _:
                return Edge_Type.INESSENTIAL
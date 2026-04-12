from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .edge import Edge

import math

from .point_enum import Point_Position

class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y

    # -------------------------
    # Operator Overloading
    # -------------------------
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Point':
        return Point(self.x * scalar, self.y * scalar)
    
    def __neg__(self):
        return Point(-self.x, -self.y)

    def __rmul__(self, scalar: float) -> 'Point':
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> 'Point':
        return Point(self.x / scalar, self.y / scalar)

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Point index out of range")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) > (other.x, other.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    # -------------------------
    # Geometry Methods
    # -------------------------

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def polar_angle(self) -> float:
        return math.atan2(self.y, self.x)

    # -------------------------
    # Classification
    # -------------------------

    def classify(self, p0: 'Point', p1: 'Point') -> Point_Position:
        """
        Classify point relative to line p0->p1
        Returns:
            Point_Position.LEFT if self is to the left of the line
            Point_Position.RIGHT if self is to the right of the line
            Point_Position.BEYOND if self is beyond p1
            Point_Position.BEHIND if self is behind p0
            Point_Position.BETWEEN if self is between p0 and p1
            Point_Position.ORIGIN if self coincides with p0
            Point_Position.DESTINATION if self coincides with p1
        """
        a = p1 - p0
        b = self - p0

        sa = a.x * b.y - a.y * b.x

        if sa > 0:
            return Point_Position.LEFT
        if sa < 0:
            return Point_Position.RIGHT

        dot = a.x * b.x + a.y * b.y

        if dot < 0:
            return Point_Position.BEHIND
        if a.length() < b.length():
            return Point_Position.BEYOND

        if self == p0:
            return Point_Position.ORIGIN
        if self == p1:
            return Point_Position.DESTINATION

        return Point_Position.BETWEEN
    
    def classify_edge(self, edge: 'Edge') -> Point_Position:
        return self.classify(edge.org, edge.dest)

    def distance(self, edge: 'Edge') -> Optional[float]:
        """Distance from point to edge."""
        from .edge import Edge
        ab = Edge(edge.org, edge.dest)
        ab.flip().rot() # rotate 90 ccw
        n = ab.dest - ab.org  # Normal to edge
        n = n / n.length()  # Normalize
        f = Edge(self, self + n)  # Line from point in direction of normal
        _, t = f.intersect(edge)
        return t
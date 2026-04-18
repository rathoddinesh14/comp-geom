from .point3d import Point3D
from .point_enum import Point3D_Position
from .intersect_enum import Intersection_Type
from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from .triangle3d import Triangle3D

class Edge3D:

    def __init__(self, start: Optional['Point3D'] = None, end: Optional['Point3D'] = None) -> None:
        self.org = start if start is not None else Point3D()
        self.dest = end if end is not None else Point3D()

    def __repr__(self) -> str:
        return f"Edge3D({self.org}, {self.dest})"
    
    def point_at(self, t: float) -> 'Point3D':
        """Returns the point at parameter t on the edge."""
        return self.org + t * (self.dest - self.org)
    
    def intersect(self, t: 'Triangle3D') -> Tuple[Intersection_Type, float]:
        """Returns the intersection point of the edge with a triangle, if it exists."""
        a = self.org
        b = self.dest
        c = t[0]    # some point on the plane
        n = t.n()   # normal vector of the plane
        d = n.dot(b - a)

        if abs(d) < 1e-6:
            if self.org.classify(t) == Point3D_Position.ON:
                return Intersection_Type.COLLINEAR, 0.0
            else:
                return Intersection_Type.PARALLEL, 0.0
        num = n.dot(a - c)
        t_param = -num / d
        return Intersection_Type.SKEW, t_param
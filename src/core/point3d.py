from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .edge import Edge
    from .triangle3d import Triangle3D

import math

from .point_enum import Point_Position, Point3D_Position

class Point3D:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    # -------------------------
    # Operator Overloading
    # -------------------------
    def __add__(self, other: 'Point3D') -> 'Point3D':
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Point3D') -> 'Point3D':
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Point3D':
        return Point3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __neg__(self):
        return Point3D(-self.x, -self.y, -self.z)

    def __rmul__(self, scalar: float) -> 'Point3D':
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> 'Point3D':
        return Point3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Point index out of range")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point3D):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z, other.z)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Point3D):
            return NotImplemented
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Point3D):
            return NotImplemented
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Point3D):
            return NotImplemented
        return (self.x, self.y, self.z) > (other.x, other.y, other.z)

    def __repr__(self) -> str:
        return f"Point3D({self.x}, {self.y}, {self.z})"

    # -------------------------
    # Geometry Methods
    # -------------------------

    def length(self) -> float:
        return math.hypot(self.x, self.y, self.z)

    def dot(self, other: 'Point3D') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Point3D') -> 'Point3D':
        return Point3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def classify(self, tri: 'Triangle3D') -> Point3D_Position:
        """Classifies the point with respect to a triangle."""
        v = self - tri[0]
        l = v.length()
        if l < 1e-12:
            return Point3D_Position.ON
        
        v = v / l
        d = v.dot(tri.n())
        if math.isclose(d, 0.0):
            return Point3D_Position.ON
        elif d > 0:
            return Point3D_Position.POSITIVE
        else:
            return Point3D_Position.NEGATIVE
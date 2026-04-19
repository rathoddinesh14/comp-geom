from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.edge import Edge

from .point import Point

def dot(a: Point, b: Point) -> float:
    """Dot product of two points treated as vectors."""
    return a.x * b.x + a.y * b.y

def orientation(p: Point, q: Point, r: Point) -> float:
    """Returns the orientation of the triplet (p, q, r).
    > 0 if counter-clockwise
    < 0 if clockwise
    = 0 if collinear
    """
    a = q - p
    b = r - p
    return a.x * b.y - a.y * b.x

def polarCmp(a: Point, b: Point) -> int:
    """Compare two points by their polar angle"""
    pa = a.polar_angle()
    pb = b.polar_angle()
    if pa < pb:
        return -1
    elif pa > pb:
        return 1
    else:
        # If polar angles are the same, compare by distance from the origin
        da = a.length()
        db = b.length()
        if da < db:
            return -1
        elif da > db:
            return 1
        else:
            return 0
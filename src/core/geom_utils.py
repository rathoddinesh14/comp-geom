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
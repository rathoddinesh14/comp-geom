from typing import Callable, Optional, cast

from .point import Point
from .polygon import Polygon
from .vertex import Vertex
from .point_enum import Point_Position
from .rotation_enum import Rotation

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

def pointInPolygon(point: Point, polygon: Polygon) -> bool:
    """Determines if a point is inside a polygon."""
    if polygon.size() == 1:
        return polygon.point() == point
    if (polygon.size() == 2):
        e = polygon.edge()
        if e and point.classify_edge(e) in (Point_Position.ORIGIN, Point_Position.DESTINATION, Point_Position.BETWEEN):
            return True
    ori_v = polygon.v()
    if ori_v:
        for _ in range(polygon.size()):
            e = polygon.edge()
            if e and point.classify_edge(e) == Point_Position.RIGHT:
                polygon.set_v(ori_v)
                return False
            polygon.advance(Rotation.CW)
    return True


def leastVertex(polygon: Polygon, comparator: Optional[Callable] = None) -> Vertex:
    """Return the least vertex in *polygon* under the given ordering.

    Parameters
    ----------
    polygon:
        The polygon to search.  Must be non-None and non-empty.
    comparator:
        Optional callable ``comparator(a, b) -> bool`` that returns ``True``
        when vertex *a* is strictly less than vertex *b*.  When ``None`` the
        default lexicographic order defined by ``Point.__lt__`` is used.

    Returns
    -------
    Vertex
        The minimal vertex under the active ordering.

    Raises
    ------
    TypeError
        If *polygon* is ``None``.
    ValueError
        If *polygon* is empty (``polygon.size() == 0``).
    TypeError
        If *comparator* is not ``None`` and not callable.
    """
    if polygon is None:
        raise TypeError("polygon must not be None")
    if polygon.size() == 0:
        raise ValueError("polygon must not be empty")
    if comparator is not None and not callable(comparator):
        raise TypeError("comparator must be callable or None")

    saved_v = polygon._v
    least = polygon._v

    for _ in range(polygon.size() - 1):
        current = polygon.advance(Rotation.CW)
        if comparator is not None:
            if comparator(current, least):
                least = current
        else:
            if cast(Point, current) < cast(Point, least):
                least = current

    polygon._v = saved_v
    return cast(Vertex, least)
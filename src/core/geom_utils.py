from .point import Point
from .polygon import Polygon
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
    if (polygon.size() == 1 and polygon.point() == point):
        return True
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
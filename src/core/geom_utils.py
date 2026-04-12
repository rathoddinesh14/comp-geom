from .point import Point

def dot(a: Point, b: Point) -> float:
    """Dot product of two points treated as vectors."""
    return a.x * b.x + a.y * b.y
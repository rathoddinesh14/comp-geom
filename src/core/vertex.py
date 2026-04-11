from typing import Optional

from src.core.node import Node
from src.core.point import Point
from src.core.rotation_enum import Rotation

class Vertex(Node, Point):
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        Node.__init__(self)
        Point.__init__(self, x, y)

    @classmethod
    def from_point(cls, p: Point) -> 'Vertex':
        return cls(p.x, p.y)

    # -------------------------
    # Navigation
    # -------------------------

    def cw(self) -> 'Vertex':
        """Clockwise neighbor (next)."""
        return self.next  # type: ignore

    def ccw(self) -> 'Vertex':
        """Counter-clockwise neighbor (prev)."""
        return self.prev  # type: ignore

    def neighbor(self, rotation: Rotation) -> 'Vertex':
        """Return neighbor based on rotation (ccw,cw)."""
        if rotation == Rotation.CCW:
            return self.ccw()
        elif rotation == Rotation.CW:
            return self.cw()
        return self

    # -------------------------
    # Geometry access
    # -------------------------

    def point(self) -> Point:
        return self

    # -------------------------
    # Linked list operations
    # -------------------------

    def insert(self, node: Optional[Node]) -> 'Vertex':
        """Insert vertex after this one."""
        return super().insert(node)  # type: ignore

    def remove(self) -> 'Vertex':
        """Remove this vertex from list."""
        return super().remove()  # type: ignore

    def splice(self, node: Optional[Node]) -> None:
        """Splice operation (swap connections)."""
        super().splice(node)  # type: ignore

    # -------------------------
    # Split operation
    # -------------------------

    def split(self, v: 'Vertex') -> 'Vertex':
        """
        Split the polygon by connecting self and v.
        Returns the new vertex created (copy of self).
        """

        # Create duplicates
        a_copy = Vertex.from_point(self.point())
        b_copy = Vertex.from_point(v.point())

        # Insert copies
        self.insert(a_copy)
        v.ccw().insert(b_copy)

        # Splice
        self.splice(b_copy)

        return b_copy
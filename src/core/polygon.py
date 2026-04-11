from typing import Optional, cast

from src.core.vertex import Vertex
from src.core.point import Point
from src.core.rotation_enum import Rotation

class Polygon:
    def __init__(self, v: Optional['Vertex'] = None) -> None:
        self._v: Optional[Vertex] = v
        self._size: int = 0

        if v:
            self._recompute_size()

    # -------------------------
    # Internal helper
    # -------------------------

    def _recompute_size(self) -> None:
        """Recalculate size by traversing circular list."""
        if not self._v:
            self._size = 0
            return

        count = 1
        current = self._v.next
        while current != self._v:
            count += 1
            current = current.next

        self._size = count

    # -------------------------
    # Accessors
    # -------------------------

    def v(self) -> Optional['Vertex']:
        return self._v

    def size(self) -> int:
        return self._size

    def point(self) -> Optional['Point']:
        return self._v.point() if self._v else None

    # -------------------------
    # Navigation
    # -------------------------

    def cw(self) -> Optional['Vertex']:
        return self._v.cw() if self._v else None

    def ccw(self) -> Optional['Vertex']:
        return self._v.ccw() if self._v else None

    def neighbor(self, rotation: Rotation) -> Optional['Vertex']:
        if not self._v:
            return None
        return self._v.neighbor(rotation)

    def advance(self, rotation: Rotation) -> Optional['Vertex']:
        """Move current vertex pointer."""
        if not self._v:
            return None

        self._v = self._v.neighbor(rotation)
        return self._v

    def set_v(self, v: 'Vertex') -> 'Vertex':
        self._v = v
        return v

    # -------------------------
    # Modification
    # -------------------------

    def insert(self, p: 'Point') -> 'Vertex':
        """Insert new vertex after current vertex."""
        new_v = Vertex.from_point(p)

        if not self._v:
            self._v = new_v
            self._size = 1
            return new_v

        self._v.insert(new_v)
        self._size += 1
        return new_v

    def remove(self) -> None:
        """Remove current vertex."""
        if not self._v:
            return

        if self._v.next == self._v:
            self._v = None
            self._size = 0
            return

        next_v = cast('Vertex', self._v.next)
        self._v.remove()
        self._v = next_v
        self._size -= 1

    # -------------------------
    # Split
    # -------------------------

    def split(self, v: 'Vertex') -> Optional['Polygon']:
        """
        Split polygon into two using vertex v.
        Returns new polygon.
        """
        if not self._v or not v:
            return None

        new_vertex = self._v.split(v)

        new_polygon = Polygon(new_vertex)
        new_polygon._recompute_size()

        self._recompute_size()

        return new_polygon
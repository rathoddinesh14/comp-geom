from typing import Callable, Optional, cast

from src.core.point_enum import Point_Position

from .edge import Edge
from .vertex import Vertex
from .point import Point
from .rotation_enum import Rotation
from .geom_utils import polarCmp

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

    def edge(self):
        """Get edge from current vertex."""
        if not self._v:
            return None
        a = self.point()
        b = self.cw()
        return Edge(a, b.point() if b else None)

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
            return self._v

        self._v = self._v.insert(new_v)
        self._size += 1
        return self._v

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
    
    def pointInPolygon(self, point: Point) -> bool:
        """Determines if a point is inside a polygon."""
        if self.size() == 1:
            return self.point() == point
        if (self.size() == 2):
            e = self.edge()
            if e and point.classify_edge(e) in (Point_Position.ORIGIN, Point_Position.DESTINATION, Point_Position.BETWEEN):
                return True
        ori_v = self.v()
        if ori_v:
            for _ in range(self.size()):
                e = self.edge()
                if e and point.classify_edge(e) == Point_Position.RIGHT:
                    self.set_v(ori_v)
                    return False
                self.advance(Rotation.CW)
        return True
    
    def leastVertex(self, comparator: Optional[Callable] = None) -> Vertex:
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
        if self is None:
            raise TypeError("polygon must not be None")
        if self.size() == 0:
            raise ValueError("polygon must not be empty")
        if comparator is not None and not callable(comparator):
            raise TypeError("comparator must be callable or None")

        saved_v = self._v
        least = self._v

        for _ in range(self.size() - 1):
            current = self.advance(Rotation.CW)
            if comparator is not None:
                if comparator(current, least):
                    least = current
            else:
                if cast(Point, current) < cast(Point, least):
                    least = current

        self._v = saved_v
        return cast(Vertex, least)
    
    def star_polygonize(self, vertices: list[Vertex]) -> None:
        """Polygonize a star-shaped polygon given its vertices."""
        if not vertices:
            return

        start_v = vertices[0]
        self.insert(start_v)

        for v in vertices[1:]:
            self.set_v(start_v)
            self.advance(Rotation.CW)
            while(polarCmp(v, cast(Point, self.point())) < 0):
                self.advance(Rotation.CW)
            self.advance(Rotation.CCW)
            self.insert(v)
        
        self.set_v(start_v)

    def plot(self, show_points: bool = True, show_labels: bool = False, title: str = "Polygon with Current Vertex Highlighted") -> None:
        """Plot polygon and highlight current vertex (_v)."""
        import matplotlib.pyplot as plt

        if not self._v:
            print("Empty polygon")
            return

        points = []
        start = self._v
        current = start

        # Collect vertices
        while True:
            p = cast(Point, current)
            points.append((p.x, p.y, current))  # store vertex reference too
            current = current.next
            if current == start:
                break

        # Close polygon
        coords = [(x, y) for x, y, _ in points]
        coords.append(coords[0])

        xs, ys = zip(*coords)

        plt.figure()
        plt.plot(xs, ys, '-o', color='blue', label="Edges")

        # Plot all points
        if show_points:
            px = [x for x, y, _ in points]
            py = [y for x, y, _ in points]
            plt.scatter(px, py, color='blue')

        # 🔥 Highlight current vertex (_v)
        current_p = self._v.point()
        plt.scatter(
            [current_p.x],
            [current_p.y],
            color='red',
            s=120,
            zorder=5,
            label="Current Vertex (_v)"
        )

        # Optional labels
        if show_labels:
            for i, (x, y, _) in enumerate(points):
                plt.text(x, y, f"{i}", fontsize=10)

        # Geometric accuracy
        plt.gca().set_aspect('equal', adjustable='box')

        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()
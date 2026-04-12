"""Unit tests for the Polygon class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import cast
from src.core.polygon import Polygon
from src.core.vertex import Vertex
from src.core.rotation_enum import Rotation


class TestPolygon:
    """Test cases for Polygon class."""

    def test_init_default(self):
        """Test default initialization."""
        poly = Polygon()
        assert poly._v is None
        assert poly._size == 0

    def test_init_with_vertex(self):
        """Test initialization with a vertex."""
        v = Vertex(1, 2)
        poly = Polygon(v)
        assert poly._v == v
        assert poly._size == 1

    def test_insert(self):
        """Test inserting vertices."""
        poly = Polygon()
        v1 = poly.insert(Vertex(1, 2))
        assert poly._v == v1
        assert poly._size == 1

        v2 = poly.insert(Vertex(3, 4))
        assert poly._v == v1
        assert poly._size == 2
        assert v1.next == v2
        assert v2.prev == v1

    def test_remove(self):
        """Test removing vertices."""
        poly = Polygon()
        v1 = poly.insert(Vertex(1, 2))
        v2 = poly.insert(Vertex(3, 4))

        poly.remove()
        assert poly._v == v2
        assert poly._size == 1
        assert v2.next == v2
        assert v2.prev == v2

        poly.remove()
        assert poly._v is None
        assert poly._size == 0

    def test_vertex_navigation(self):
        """Test vertex navigation."""
        poly = Polygon()
        v1 = poly.insert(Vertex(1, 2))
        v2 = poly.insert(Vertex(3, 4))
        v3 = poly.insert(Vertex(5, 6))

        assert poly._v == v1
        assert poly.neighbor(Rotation.CW) == v3
        assert poly.neighbor(Rotation.CCW) == v2

        poly.advance(Rotation.CW)
        assert poly._v == v3
        poly.advance(Rotation.CCW)
        assert poly._v == v1

    def test_split(self):
        """Test splitting the polygon."""
        poly = Polygon()
        v1 = poly.insert(Vertex(1, 2))
        v2 = poly.insert(Vertex(3, 4))
        v3 = poly.insert(Vertex(5, 6))
        v4 = poly.insert(Vertex(7, 8))
        v5 = poly.insert(Vertex(9, 10))
        v6 = poly.insert(Vertex(11, 12))

        new_poly = poly.split(v4)
        assert new_poly is not None
        assert poly._size == 4
        assert new_poly._size == 4
        assert poly._v is v1
        assert new_poly._v is not v4
        assert poly.neighbor(Rotation.CW) is v4
        assert cast(Vertex, new_poly.neighbor(Rotation.CW)).point() == v1.point()
"""Unit tests for the Vertex class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import pytest
from src.core.point import Point
from src.core.rotation_enum import Rotation
from src.core.vertex import Vertex

class TestVertex:
    """Test cases for Vertex class."""

    def test_init_default(self):
        """Test default initialization."""
        v = Vertex()
        assert v.x == 0.0
        assert v.y == 0.0
        assert v.next == v
        assert v.prev == v

    def test_init_with_values(self):
        """Test initialization with values."""
        p = Point(1.5, -2.3)
        v = Vertex.from_point(p)
        assert v.x == 1.5
        assert v.y == -2.3
        assert v.next == v
        assert v.prev == v

    @pytest.fixture
    def sample_vertices(self) -> tuple[Vertex, Vertex, Vertex]:
        """Fixture to create a sample vertex list."""
        v1 = Vertex(0, 0)
        v2 = Vertex(1, 0)
        v3 = Vertex(1, 1)
        v1.insert(v2)
        v2.insert(v3)
        return v1, v2, v3

    def test_navigation(self, sample_vertices):
        """Test navigation methods."""
        v1, v2, v3 = sample_vertices

        assert v1.cw() == v2
        assert v2.cw() == v3
        assert v3.cw() == v1

        assert v1.ccw() == v3
        assert v2.ccw() == v1
        assert v3.ccw() == v2

    def test_neighbor(self, sample_vertices):
        """Test neighbor method with rotation."""
        v1, v2, v3 = sample_vertices

        assert v1.neighbor(Rotation.CCW) == v3
        assert v1.neighbor(Rotation.CW) == v2
        assert v1.neighbor(None) == v1  # No rotation case

    def test_point(self):
        """Test point method."""
        v = Vertex(2.5, 3.5)
        p = v.point()
        assert isinstance(p, Point)
        assert p.x == 2.5
        assert p.y == 3.5

    def test_insert_and_remove(self):
        """Test insert and remove operations."""
        v1 = Vertex(0, 0)
        v2 = Vertex(1, 0)
        v3 = Vertex(1, 1)

        v1.insert(v2)
        v2.insert(v3)

        assert v1.cw() == v2
        assert v2.cw() == v3
        assert v3.cw() == v1
        assert v3.ccw() == v2

        # Remove v2 and check connections
        v2.remove()
        assert v1.cw() == v3
        assert v3.ccw() == v1

    def test_splice(self, sample_vertices):
        """Test splice operation."""
        v1, v2, v3 = sample_vertices
        v4 = Vertex(2, 2)
        v5 = Vertex(3, 3)

        # Create a new list with v4 and v5
        v4.insert(v5)

        # Splice the new list after v1
        v1.splice(v4)

        assert v1.cw() == v5
        assert v4.cw() == v2
        assert v5.cw() == v4

    def test_split(self, sample_vertices):
        """Test split operation."""
        v1, v2, v3 = sample_vertices
        v4 = Vertex(0.5, 0.5)
        v3.insert(v4)
        # Split between v1 and v2
        new_v = v1.split(v3)

        assert new_v is not None
        assert new_v.point() == v3.point()
        assert v1.cw() == v3
        assert new_v.cw().point() == v1.point()

    def test_equality(self):
        """Test equality comparison."""
        v1 = Vertex(1, 2)
        v2 = Vertex(1, 2)
        v3 = Vertex(2, 3)
        v4 = v1

        assert v1 == v2
        assert v1 != v3
        assert v1 == v4
"""Unit tests for the GeomUtils class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import pytest
from src.core.point import Point
from src.core.polygon import Polygon
from src.core.vertex import Vertex
from src.core.geom_utils import dot, orientation, polarCmp

class TestGeomUtils:
    """Test cases for GeomUtils class."""

    def test_dot(self):
        """Test dot product."""
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        result = dot(p1, p2)
        assert math.isclose(result, 11.0)

    def test_orientation(self):
        """Test orientation."""
        p = Point(0, 0)
        q = Point(1, 0)
        r = Point(0, 1)
        result = orientation(p, q, r)
        assert result > 0  # Counter-clockwise

        r = Point(0, -1)
        result = orientation(p, q, r)
        assert result < 0  # Clockwise

        r = Point(2, 0)
        result = orientation(p, q, r)
        assert math.isclose(result, 0.0)  # Collinear

    def test_polarCmp(self):
        """Test polarCmp."""
        p1 = Point(1, 0)
        p2 = Point(0, 1)
        result = polarCmp(p1, p2)
        assert result < 0  # p1 has smaller polar angle than p2

        p1 = Point(0, 1)
        p2 = Point(1, 0)
        result = polarCmp(p1, p2)
        assert result > 0  # p1 has larger polar angle than p2

        p1 = Point(1, 1)
        p2 = Point(1, 1)
        result = polarCmp(p1, p2)
        assert result == 0  # Both points have the same polar angle

        p1 = Point(1, 1)
        p2 = Point(2, 2)
        result = polarCmp(p1, p2)
        assert result < 0  # p1 has smaller polar angle than p2 (both are at 45 degrees, but p1 is closer to the origin)
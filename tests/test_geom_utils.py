"""Unit tests for the GeomUtils class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import pytest
from src.core.point import Point
from src.core.polygon import Polygon
from src.core.vertex import Vertex
from src.core.point_enum import Point_Position
from src.core.geom_utils import dot, orientation, pointInPolygon

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

    def test_point_in_polygon_trivial(self):
        """Test point in polygon with a trivial case."""
        point = Point(0.5, 0.5)
        polygon = Polygon(Vertex.from_point(point))
        result = pointInPolygon(point, polygon)
        assert result == True

        point_outside = Point(1.5, 1.5)
        result = pointInPolygon(point_outside, polygon)
        assert result == False

    def test_point_in_polygon_edge(self):
        """Test point in polygon with a point on the edge."""
        v1 = Vertex(0, 0)
        v2 = Vertex(1, 0)
        polygon = Polygon(v1)
        polygon.insert(v2)

        point_on_edge = Point(0.5, 0)
        result = pointInPolygon(point_on_edge, polygon)
        assert result == True

        point_outside = Point(0.5, -0.5)
        result = pointInPolygon(point_outside, polygon)
        assert result == False

    def test_point_in_polygon_complex(self):
        """Test point in polygon with a more complex polygon."""
        v1 = Vertex(0, 0)
        v2 = Vertex(2, 0)
        v3 = Vertex(2, 2)
        v4 = Vertex(0, 2)
        polygon = Polygon(v1)
        polygon.insert(v2)
        polygon.insert(v3)
        polygon.insert(v4)

        point_inside = Point(1, 1)
        result = pointInPolygon(point_inside, polygon)
        assert result == True

        point_outside = Point(3, 3)
        result = pointInPolygon(point_outside, polygon)
        assert result == False
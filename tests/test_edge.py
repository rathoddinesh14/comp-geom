"""Unit tests for the Edge class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import pytest
from src.core.point import Point
from src.core.edge import Edge
from src.core.intersect_enum import Intersection_Type


class TestEdge:
    """Test cases for Edge class."""

    def test_init_default(self):
        """Test default initialization."""
        e = Edge()
        assert e.org.x == 0.0 and e.org.y == 0.0
        assert e.dest.x == 1.0 and e.dest.y == 0.0

    def test_init_with_points(self):
        """Test initialization with specific points."""
        org = Point(1, 2)
        dest = Point(3, 4)
        e = Edge(org, dest)
        assert e.org == org
        assert e.dest == dest

    def test_rot(self):
        """Test edge rotation."""
        e = Edge(Point(0, 0), Point(2, 0))
        e.rot()
        assert math.isclose(e.org.x, 1.0) and math.isclose(e.org.y, 1.0)
        assert math.isclose(e.dest.x, 1.0) and math.isclose(e.dest.y, -1.0)

    def test_flip(self):
        """Test edge flipping."""
        org = Point(1, 2)
        dest = Point(3, 4)
        e = Edge(org, dest)
        e.flip()
        assert e.org == dest
        assert e.dest == org

    def test_point(self):
        """Test parametric point calculation."""
        e = Edge(Point(0, 0), Point(2, 2))
        p_mid = e.point(0.5)
        assert p_mid == Point(1, 1)

    def test_is_vertical(self):
        """Test vertical edge detection."""
        e1 = Edge(Point(1, 0), Point(1, 2))
        e2 = Edge(Point(0, 0), Point(2, 0))
        assert e1.is_vertical() is True
        assert e2.is_vertical() is False

    def test_slope(self):
        """Test slope calculation."""
        e = Edge(Point(0, 0), Point(2, 2))
        assert math.isclose(e.slope(), 1.0)
        e_vertical = Edge(Point(1, 0), Point(1, 2))
        assert math.isinf(e_vertical.slope())

    def test_y_intercept(self):
        """Test y-intercept calculation."""
        e = Edge(Point(0, 1), Point(2, 3))
        assert math.isclose(e.y(0), 1.0)
        assert math.isclose(e.y(1), 2.0)
        assert math.isclose(e.y(2), 3.0)
        e_vertical = Edge(Point(1, 0), Point(1, 2))
        with pytest.raises(ValueError):
            e_vertical.y(0)

    def test_intersection(self):
        """Test edge intersection."""
        e1 = Edge(Point(0, 0), Point(2, 2))
        e2 = Edge(Point(0, 2), Point(2, 0))
        intersects, t = e1.intersect(e2)
        assert intersects is Intersection_Type.SKEW
        assert t is not None
        assert math.isclose(t, 0.5)

        e_parallel = Edge(Point(0, 0), Point(2, 0))
        e_parallel2 = Edge(Point(0, 1), Point(2, 1))
        intersects, t = e_parallel.intersect(e_parallel2)
        assert intersects is Intersection_Type.PARALLEL
        assert t is None

        e_collinear = Edge(Point(0, 0), Point(2, 0))
        e_collinear2 = Edge(Point(1, 0), Point(3, 0))
        intersects, t = e_collinear.intersect(e_collinear2)
        assert intersects is Intersection_Type.COLLINEAR
        assert t is None

    def test_intersection_endpoint(self):
        """Test intersection at edge endpoints."""
        e1 = Edge(Point(0, 0), Point(2, 2))
        e2 = Edge(Point(2, 2), Point(4, 3))
        intersects, t = e1.intersect(e2)
        assert intersects is Intersection_Type.SKEW
        assert t is not None
        assert math.isclose(t, 1.0)

    def test_cross(self):
        """Test segment intersection."""
        e1 = Edge(Point(0, 0), Point(2, 2))
        e2 = Edge(Point(0, 2), Point(2, 0))
        cross_type, t = e1.cross(e2)
        assert cross_type is Intersection_Type.SKEW_CROSS
        assert t is not None
        assert math.isclose(t, 0.5)

        e_parallel = Edge(Point(0, 0), Point(2, 0))
        e_parallel2 = Edge(Point(0, 1), Point(2, 1))
        cross_type, t = e_parallel.cross(e_parallel2)
        assert cross_type is Intersection_Type.PARALLEL
        assert t is None

        e_collinear = Edge(Point(0, 0), Point(2, 0))
        e_collinear2 = Edge(Point(1, 0), Point(3, 0))
        cross_type, t = e_collinear.cross(e_collinear2)
        assert cross_type is Intersection_Type.COLLINEAR
        assert t is None

        e_no_cross = Edge(Point(0, 0), Point(1, 1))
        e_no_cross2 = Edge(Point(2, 2), Point(3, 2))
        cross_type, t = e_no_cross.cross(e_no_cross2)
        assert cross_type is Intersection_Type.SKEW_NO_CROSS
        assert t is None

        cross_type, t = e_no_cross2.cross(e_no_cross)
        assert cross_type is Intersection_Type.SKEW_NO_CROSS
        assert t is None

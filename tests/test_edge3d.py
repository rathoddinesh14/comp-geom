"""Unit tests for the Edge3D class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import pytest
from src.core.point3d import Point3D
from src.core.edge3d import Edge3D
from src.core.triangle3d import Triangle3D

from src.core.intersect_enum import Intersection_Type


class TestEdge3D:
    """Test cases for Edge3D class."""

    def test_init_default(self):
        """Test default initialization."""
        e = Edge3D()
        assert e.org.x == 0.0 and e.org.y == 0.0 and e.org.z == 0.0
        assert e.dest.x == 0.0 and e.dest.y == 0.0 and e.dest.z == 0.0

    def test_init_with_points(self):
        """Test initialization with specific points."""
        org = Point3D(1, 2, 3)
        dest = Point3D(4, 5, 6)
        e = Edge3D(org, dest)
        assert e.org == org
        assert e.dest == dest


    def test_point_at(self):
        """Test parametric point calculation."""
        e = Edge3D(Point3D(0, 0, 0), Point3D(2, 2, 0))
        p_mid = e.point_at(0.5)
        assert p_mid == Point3D(1, 1, 0)

    def test_intersect_t_1(self):
        """Test edge-triangle intersection."""
        e = Edge3D(Point3D(0, 0, 0), Point3D(1, 1, 1))
        tri = Triangle3D(Point3D(0, 0, 1), Point3D(1, 0, 1), Point3D(0, 1, 1))
        result = e.intersect(tri)
        assert isinstance(result, tuple)
        assert isinstance(result[0], Intersection_Type)
        assert isinstance(result[1], float)
        assert result[0] == Intersection_Type.SKEW
        assert math.isclose(result[1], 1.0, abs_tol=1e-6)

    def test_intersect_t_2(self):
        """Test edge-triangle intersection."""
        e = Edge3D(Point3D(0, 0, 0), Point3D(1, 1, 0.5))
        tri = Triangle3D(Point3D(0, 0, 1), Point3D(1, 0, 1), Point3D(0, 1, 1))
        result = e.intersect(tri)
        assert isinstance(result, tuple)
        assert isinstance(result[0], Intersection_Type)
        assert isinstance(result[1], float)
        assert result[0] == Intersection_Type.SKEW
        assert math.isclose(result[1], 2.0, abs_tol=1e-6)

    def test_intersect_t_3(self):
        """Test edge-triangle intersection."""
        e = Edge3D(Point3D(0, 0, 0), Point3D(1, 1, 1))
        tri = Triangle3D(Point3D(0, 0, -2), Point3D(1, 0, -2), Point3D(0, 1, -2))
        result = e.intersect(tri)
        assert isinstance(result, tuple)
        assert isinstance(result[0], Intersection_Type)
        assert isinstance(result[1], float)
        assert result[0] == Intersection_Type.SKEW
        assert math.isclose(result[1], -2, abs_tol=1e-6)

    def test_intersect_parallel(self):
        """Test edge parallel to triangle."""
        e = Edge3D(Point3D(0, 0, 0), Point3D(1, 0, 0))
        tri = Triangle3D(Point3D(0, 0, 1), Point3D(1, 0, 1), Point3D(0, 1, 1))
        result = e.intersect(tri)
        assert result[0] == Intersection_Type.PARALLEL

    def test_intersect_collinear(self):
        """Test edge collinear with triangle."""
        e = Edge3D(Point3D(0, 0, 1), Point3D(1, 0, 1))
        tri = Triangle3D(Point3D(0, 0, 1), Point3D(1, 0, 1), Point3D(0, 1, 1))
        result = e.intersect(tri)
        assert result[0] == Intersection_Type.COLLINEAR


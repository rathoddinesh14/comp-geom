"""Unit tests for the Triangle3D class."""

import sys
import os

from src.core.intersect_enum import Intersection_Type

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.edge3d import Edge3D
from src.core.rotation_enum import Rotation
from src.core.triangle3d import Triangle3D
from src.core.point3d import Point3D
from src.core.point import Point

class TestTriangle3D:
    """Test cases for Triangle3D class."""

    def test_init_default(self):
        """Test default initialization."""
        tri = Triangle3D(Point3D(), Point3D(), Point3D())
        assert tri[0] == Point3D()
        assert tri[1] == Point3D()
        assert tri[2] == Point3D()
        assert tri._id == 0
        assert tri._bounding_box.org == Point3D()
        assert tri._bounding_box.dest == Point3D()

    def test_normal_vector(self):
        """Test normal vector computation."""
        tri = Triangle3D(Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(0, 1, 0))
        n = tri.n()
        assert n == Point3D(0, 0, 1)

    def test_projection(self):
        """Test projection of triangle onto 2D plane."""
        tri = Triangle3D(Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(0, 1, 0))
        poly = tri.project(0, 1)
        assert poly.size() == 3
        assert poly.v() == Point(0, 1)
        poly.advance(Rotation.CW)
        assert poly.v() == Point(1, 0)
        poly.advance(Rotation.CW)
        assert poly.v() == Point(0, 0)

    def test_line_triangle_intersect(self):
        """Test line-triangle intersection."""
        tri = Triangle3D(Point3D(0, 0, 0), Point3D(0, 1, 0), Point3D(1, 0, 0))
        edge = Edge3D(Point3D(0.5, 0.5, -1), Point3D(0.5, 0.5, 1))
        intersect_type, t = tri.lineTriangleIntersect(edge)
        assert intersect_type == Intersection_Type.SKEW_CROSS
        
        edge_no_cross = Edge3D(Point3D(1.5, 1.5, -1), Point3D(1.5, 1.5, 1))
        intersect_type_no_cross, t_no_cross = tri.lineTriangleIntersect(edge_no_cross)
        assert intersect_type_no_cross == Intersection_Type.SKEW_NO_CROSS


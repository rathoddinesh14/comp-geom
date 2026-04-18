"""Unit tests for the Point class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import pytest
from src.core.point3d import Point3D


class TestPoint3D:
    """Test cases for Point3D class."""

    def test_init_default(self):
        """Test default initialization."""
        p = Point3D()
        assert p.x == 0.0
        assert p.y == 0.0
        assert p.z == 0.0

    def test_init_with_values(self):
        """Test initialization with values."""
        p = Point3D(1.5, -2.3, 0.0)
        assert p.x == 1.5
        assert p.y == -2.3
        assert p.z == 0.0

    def test_add(self):
        """Test point addition."""
        p1 = Point3D(1, 2, 0)
        p2 = Point3D(3, 4, 0)
        result = p1 + p2
        assert result.x == 4
        assert result.y == 6
        assert result.z == 0
        # Ensure original points are unchanged
        assert p1.x == 1 and p1.y == 2 and p1.z == 0
        assert p2.x == 3 and p2.y == 4 and p2.z == 0

    def test_sub(self):
        """Test point subtraction."""
        p1 = Point3D(5, 7, 0)
        p2 = Point3D(2, 3, 0)
        result = p1 - p2
        assert result.x == 3
        assert result.y == 4
        assert result.z == 0

    def test_mul(self):
        """Test scalar multiplication."""
        p = Point3D(2, 3, 0)
        result = p * 2.5
        assert result.x == 5.0
        assert result.y == 7.5
        assert result.z == 0

    def test_rmul(self):
        """Test right scalar multiplication."""
        p = Point3D(2, 3, 0)
        result = 2.5 * p
        assert result.x == 5.0
        assert result.y == 7.5
        assert result.z == 0

    def test_truediv(self):
        """Test scalar division."""
        p = Point3D(5, 10, 0)
        result = p / 2
        assert result.x == 2.5
        assert result.y == 5.0
        assert result.z == 0

    def test_getitem(self):
        """Test indexing."""
        p = Point3D(1.5, -2.3, 0)
        assert p[0] == 1.5
        assert p[1] == -2.3
        assert p[2] == 0

    def test_getitem_out_of_range(self):
        """Test indexing with invalid index."""
        p = Point3D(1, 2, 0)
        with pytest.raises(IndexError):
            _ = p[3]

    def test_eq(self):
        """Test equality."""
        p1 = Point3D(1, 2, 0)
        p2 = Point3D(1, 2, 0)
        p3 = Point3D(1.0000000001, 2, 0)  # Close but not equal due to floating point
        p4 = Point3D(2, 2, 0)

        assert p1 == p2
        assert p1 != p4
        # Test floating point precision
        assert p1 == p3  # Should be close enough

    def test_eq_different_type(self):
        """Test equality with different type."""
        p = Point3D(1, 2, 0)
        assert p != "not a point"
        assert p != 42

    def test_ne(self):
        """Test inequality."""
        p1 = Point3D(1, 2, 0)
        p2 = Point3D(2, 3, 0)
        assert p1 != p2

    def test_lt(self):
        """Test less than comparison."""
        p1 = Point3D(1, 2, 0)
        p2 = Point3D(2, 2, 0)
        p3 = Point3D(1, 3, 0)
        assert p1 < p2
        assert p1 < p3
        assert not (p2 < p1)

    def test_lt_different_type(self):
        """Test less than with different type."""
        p = Point3D(1, 2, 0)
        with pytest.raises(TypeError):
            p < "not a point"

    def test_gt(self):
        """Test greater than comparison."""
        p1 = Point3D(2, 2, 0)
        p2 = Point3D(1, 2, 0)
        assert p1 > p2

    def test_repr(self):
        """Test string representation."""
        p = Point3D(1.5, -2.3, 0)
        assert repr(p) == "Point3D(1.5, -2.3, 0)"

    def test_length(self):
        """Test length calculation."""
        p = Point3D(3, 4, 0)
        assert p.length() == 5.0

        p_zero = Point3D(0, 0, 0)
        assert p_zero.length() == 0.0

    def test_dot(self):
        """Test dot product."""
        p1 = Point3D(1, 2, 3)
        p2 = Point3D(4, 5, 6)
        result = p1.dot(p2)
        assert result == 32  # 1*4 + 2*5 + 3*6

    def test_dot_orthogonal(self):
        """Test dot product of orthogonal vectors."""
        p1 = Point3D(1, 0, 0)
        p2 = Point3D(0, 1, 0)
        result = p1.dot(p2)
        assert result == 0

    def test_dot_parallel(self):
        """Test dot product of parallel vectors."""
        p1 = Point3D(1, 2, 3)
        p2 = Point3D(2, 4, 6)  # p2 is 2 * p1
        result = p1.dot(p2)
        assert result == 28  # 1*2 + 2*4 + 3*6

    def test_dot_zero_vector(self):
        """Test dot product with zero vector."""
        p1 = Point3D(1, 2, 3)
        p_zero = Point3D(0, 0, 0)
        result = p1.dot(p_zero)
        assert result == 0
    
    def test_dot_self(self):
        """Test dot product of a vector with itself."""
        p = Point3D(1, 2, 3)
        result = p.dot(p)
        assert result == 14  # 1*1 + 2*2 + 3*3

    def test_cross(self):
        """Test cross product."""
        p1 = Point3D(1, 0, 0)
        p2 = Point3D(0, 1, 0)
        result = p1.cross(p2)
        assert result == Point3D(0, 0, 1)  # i x j = k

        p3 = Point3D(0, 0, 1)
        result2 = p2.cross(p3)
        assert result2 == Point3D(1, 0, 0)  # j x k = i

        result3 = p3.cross(p1)
        assert result3 == Point3D(0, 1, 0)  # k x i = j

    def test_cross_parallel(self):
        """Test cross product of parallel vectors."""
        p1 = Point3D(1, 2, 3)
        p2 = Point3D(2, 4, 6)  # p2 is 2 * p1
        result = p1.cross(p2)
        assert result == Point3D(0, 0, 0)  # Cross product of parallel vectors is zero

    def test_cross_orthogonal(self):
        """Test cross product of orthogonal vectors."""
        p1 = Point3D(1, 0, 0)
        p2 = Point3D(0, 1, 0)
        result = p1.cross(p2)
        assert result == Point3D(0, 0, 1)  # i x j = k

    def test_cross_zero_vector(self):
        """Test cross product with zero vector."""
        p1 = Point3D(1, 2, 3)
        p_zero = Point3D(0, 0, 0)
        result = p1.cross(p_zero)
        assert result == Point3D(0, 0, 0)  # Cross product with zero vector is zero
    
    def test_cross_self(self):
        """Test cross product of a vector with itself."""
        p = Point3D(1, 2, 3)
        result = p.cross(p)
        assert result == Point3D(0, 0, 0)  # Cross product of a vector with itself is zero
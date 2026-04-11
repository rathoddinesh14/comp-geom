"""Unit tests for the Point class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import pytest
from src.core.point import Point
from src.core.point_enum import Point_Position


class TestPoint:
    """Test cases for Point class."""

    def test_init_default(self):
        """Test default initialization."""
        p = Point()
        assert p.x == 0.0
        assert p.y == 0.0

    def test_init_with_values(self):
        """Test initialization with values."""
        p = Point(1.5, -2.3)
        assert p.x == 1.5
        assert p.y == -2.3

    def test_add(self):
        """Test point addition."""
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        result = p1 + p2
        assert result.x == 4
        assert result.y == 6
        # Ensure original points are unchanged
        assert p1.x == 1 and p1.y == 2
        assert p2.x == 3 and p2.y == 4

    def test_sub(self):
        """Test point subtraction."""
        p1 = Point(5, 7)
        p2 = Point(2, 3)
        result = p1 - p2
        assert result.x == 3
        assert result.y == 4

    def test_mul(self):
        """Test scalar multiplication."""
        p = Point(2, 3)
        result = p * 2.5
        assert result.x == 5.0
        assert result.y == 7.5

    def test_rmul(self):
        """Test right scalar multiplication."""
        p = Point(2, 3)
        result = 2.5 * p
        assert result.x == 5.0
        assert result.y == 7.5

    def test_getitem(self):
        """Test indexing."""
        p = Point(1.5, -2.3)
        assert p[0] == 1.5
        assert p[1] == -2.3

    def test_getitem_out_of_range(self):
        """Test indexing with invalid index."""
        p = Point(1, 2)
        with pytest.raises(IndexError):
            _ = p[2]

    def test_eq(self):
        """Test equality."""
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(1.0000000001, 2)  # Close but not equal due to floating point
        p4 = Point(2, 2)

        assert p1 == p2
        assert p1 != p4
        # Test floating point precision
        assert p1 == p3  # Should be close enough

    def test_eq_different_type(self):
        """Test equality with different type."""
        p = Point(1, 2)
        assert p != "not a point"
        assert p != 42

    def test_ne(self):
        """Test inequality."""
        p1 = Point(1, 2)
        p2 = Point(2, 3)
        assert p1 != p2

    def test_lt(self):
        """Test less than comparison."""
        p1 = Point(1, 2)
        p2 = Point(2, 2)
        p3 = Point(1, 3)
        assert p1 < p2
        assert p1 < p3
        assert not (p2 < p1)

    def test_lt_different_type(self):
        """Test less than with different type."""
        p = Point(1, 2)
        with pytest.raises(TypeError):
            p < "not a point"

    def test_gt(self):
        """Test greater than comparison."""
        p1 = Point(2, 2)
        p2 = Point(1, 2)
        assert p1 > p2

    def test_repr(self):
        """Test string representation."""
        p = Point(1.5, -2.3)
        assert repr(p) == "Point(1.5, -2.3)"

    def test_length(self):
        """Test length calculation."""
        p = Point(3, 4)
        assert p.length() == 5.0

        p_zero = Point(0, 0)
        assert p_zero.length() == 0.0

    def test_polar_angle(self):
        """Test polar angle calculation."""
        # Positive x-axis
        p = Point(1, 0)
        assert math.isclose(p.polar_angle(), 0.0)

        # Positive y-axis
        p = Point(0, 1)
        assert math.isclose(p.polar_angle(), math.pi / 2)

        # Negative x-axis
        p = Point(-1, 0)
        assert math.isclose(p.polar_angle(), math.pi)

        # Negative y-axis
        p = Point(0, -1)
        assert math.isclose(p.polar_angle(), -math.pi / 2)

    def test_classify_left(self):
        """Test point classification - left of line."""
        p0 = Point(0, 0)
        p1 = Point(1, 0)
        test_point = Point(0, 1)
        assert test_point.classify(p0, p1) == Point_Position.LEFT

    def test_classify_right(self):
        """Test point classification - right of line."""
        p0 = Point(0, 0)
        p1 = Point(1, 0)
        test_point = Point(0, -1)
        assert test_point.classify(p0, p1) == Point_Position.RIGHT

    def test_classify_behind(self):
        """Test point classification - behind p0."""
        p0 = Point(0, 0)
        p1 = Point(1, 0)
        test_point = Point(-1, 0)
        assert test_point.classify(p0, p1) == Point_Position.BEHIND

    def test_classify_beyond(self):
        """Test point classification - beyond p1."""
        p0 = Point(0, 0)
        p1 = Point(1, 0)
        test_point = Point(2, 0)
        assert test_point.classify(p0, p1) == Point_Position.BEYOND

    def test_classify_between(self):
        """Test point classification - between p0 and p1."""
        p0 = Point(0, 0)
        p1 = Point(2, 0)
        test_point = Point(1, 0)
        assert test_point.classify(p0, p1) == Point_Position.BETWEEN

    def test_classify_origin(self):
        """Test point classification - coincides with p0."""
        p0 = Point(1, 2)
        p1 = Point(3, 4)
        test_point = Point(1, 2)
        assert test_point.classify(p0, p1) == Point_Position.ORIGIN

    def test_classify_destination(self):
        """Test point classification - coincides with p1."""
        p0 = Point(1, 2)
        p1 = Point(3, 4)
        test_point = Point(3, 4)
        assert test_point.classify(p0, p1) == Point_Position.DESTINATION

    def test_classify_collinear_cases(self):
        """Test edge cases for collinear points."""
        # Points on the line but not exactly at endpoints
        p0 = Point(0, 0)
        p1 = Point(4, 0)
        test_point = Point(2, 0)  # Exactly between
        assert test_point.classify(p0, p1) == Point_Position.BETWEEN

        # Point very close to p1
        test_point = Point(3.999999, 0)
        assert test_point.classify(p0, p1) == Point_Position.BETWEEN
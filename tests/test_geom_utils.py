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


# ---------------------------------------------------------------------------
# Import leastVertex (added alongside the existing geom_utils functions)
# ---------------------------------------------------------------------------
from src.core.geom_utils import leastVertex

def _build_polygon(*coords: tuple) -> Polygon:
    """Helper: build a Polygon from an iterable of (x, y) tuples."""
    xs, ys = coords[0]
    poly = Polygon(Vertex(xs, ys))
    for x, y in coords[1:]:
        poly.insert(Vertex(x, y))
    return poly

class TestLeastVertexDefaultOrdering:
    """2.1 — Unit tests for leastVertex with default (lexicographic) ordering."""

    def test_single_vertex_returns_that_vertex(self):
        """Single-vertex polygon: the only vertex is the least."""
        poly = Polygon(Vertex(3.0, 7.0))
        result = leastVertex(poly)
        assert (result.x, result.y) == (3.0, 7.0)

    def test_two_vertex_polygon_returns_minimum(self):
        """Two-vertex polygon: the vertex with the smaller x is returned."""
        poly = _build_polygon((5.0, 1.0), (2.0, 9.0))
        result = leastVertex(poly)
        assert (result.x, result.y) == (2.0, 9.0)

    def test_multi_vertex_distinct_x_returns_smallest_x(self):
        """Multi-vertex polygon with distinct x values: smallest x wins."""
        poly = _build_polygon((4.0, 0.0), (1.0, 5.0), (3.0, 2.0), (7.0, -1.0))
        result = leastVertex(poly)
        assert result.x == 1.0

    def test_same_x_tiebreaker_by_y(self):
        """All vertices share the same x: smallest y is the tiebreaker."""
        poly = _build_polygon((2.0, 5.0), (2.0, 1.0), (2.0, 3.0))
        result = leastVertex(poly)
        assert (result.x, result.y) == (2.0, 1.0)

    def test_all_same_coordinates_any_vertex_acceptable(self):
        """All vertices share the same (x, y): any vertex is a valid answer."""
        poly = _build_polygon((1.0, 1.0), (1.0, 1.0), (1.0, 1.0))
        result = leastVertex(poly)
        assert (result.x, result.y) == (1.0, 1.0)


class TestLeastVertexErrorConditions:
    """2.2 — Unit tests for leastVertex error conditions."""

    def test_none_polygon_raises_type_error(self):
        """leastVertex(None) must raise TypeError."""
        with pytest.raises(TypeError):
            leastVertex(None)

    def test_empty_polygon_raises_value_error(self):
        """leastVertex on an empty Polygon must raise ValueError."""
        with pytest.raises(ValueError):
            leastVertex(Polygon())

    def test_comparator_int_raises_type_error(self):
        """Non-callable comparator (int) must raise TypeError."""
        poly = _build_polygon((1.0, 2.0))
        with pytest.raises(TypeError):
            leastVertex(poly, comparator=42)

    def test_comparator_string_raises_type_error(self):
        """Non-callable comparator (str) must raise TypeError."""
        poly = _build_polygon((1.0, 2.0))
        with pytest.raises(TypeError):
            leastVertex(poly, comparator="bad")

    def test_comparator_list_raises_type_error(self):
        """Non-callable comparator (list) must raise TypeError."""
        poly = _build_polygon((1.0, 2.0))
        with pytest.raises(TypeError):
            leastVertex(poly, comparator=[])


class TestLeastVertexCustomComparator:
    """2.3 — Unit tests for leastVertex with a custom comparator."""

    def test_comparator_none_same_as_no_comparator(self):
        """comparator=None must give the same result as omitting the argument."""
        poly = _build_polygon((3.0, 1.0), (1.0, 4.0), (2.0, 0.0))
        result_default = leastVertex(poly)
        result_none = leastVertex(poly, comparator=None)
        assert (result_default.x, result_default.y) == (result_none.x, result_none.y)

    def test_comparator_equivalent_to_point_lt_same_as_default(self):
        """A comparator that mirrors Point.__lt__ must return the same vertex."""
        poly = _build_polygon((5.0, 2.0), (1.0, 8.0), (3.0, 3.0))
        equiv_cmp = lambda a, b: (a.x, a.y) < (b.x, b.y)
        result_default = leastVertex(poly)
        result_custom = leastVertex(poly, comparator=equiv_cmp)
        assert (result_default.x, result_default.y) == (result_custom.x, result_custom.y)

    def test_comparator_y_first_returns_correct_vertex(self):
        """Comparator ordering by y first must return the vertex with the smallest y."""
        # Vertices: (3, 1), (1, 4), (2, 0)  — smallest y is 0 at (2, 0)
        poly = _build_polygon((3.0, 1.0), (1.0, 4.0), (2.0, 0.0))
        y_first = lambda a, b: (a.y, a.x) < (b.y, b.x)
        result = leastVertex(poly, comparator=y_first)
        assert (result.x, result.y) == (2.0, 0.0)

    def test_comparator_y_first_tiebreaker_by_x(self):
        """y-first comparator: when y values tie, smallest x wins."""
        # Vertices: (5, 2), (1, 2), (3, 4)  — y=2 ties; x=1 wins
        poly = _build_polygon((5.0, 2.0), (1.0, 2.0), (3.0, 4.0))
        y_first = lambda a, b: (a.y, a.x) < (b.y, b.x)
        result = leastVertex(poly, comparator=y_first)
        assert (result.x, result.y) == (1.0, 2.0)


class TestLeastVertexStatePreservation:
    """2.4 — Unit tests for polygon state preservation after leastVertex."""

    def test_polygon_v_unchanged_after_successful_call(self):
        """polygon._v must point to the same vertex after a successful call."""
        poly = _build_polygon((3.0, 1.0), (1.0, 4.0), (2.0, 0.0))
        original_v = poly._v
        leastVertex(poly)
        assert poly._v is original_v

    def test_polygon_v_unchanged_after_exception(self):
        """polygon._v must be unchanged even when leastVertex raises TypeError."""
        poly = _build_polygon((3.0, 1.0), (1.0, 4.0))
        original_v = poly._v
        with pytest.raises(TypeError):
            leastVertex(poly, comparator=99)
        assert poly._v is original_v

    def test_polygon_size_unchanged_after_successful_call(self):
        """polygon.size() must be the same before and after a successful call."""
        poly = _build_polygon((3.0, 1.0), (1.0, 4.0), (2.0, 0.0))
        size_before = poly.size()
        leastVertex(poly)
        assert poly.size() == size_before


# ---------------------------------------------------------------------------
# Property-Based Tests using Hypothesis
# ---------------------------------------------------------------------------
import random
import hypothesis
import hypothesis.strategies as st
from hypothesis import given, settings, HealthCheck


def _build_polygon_from_coords(coords):
    """Build a Polygon from a list of (x, y) tuples."""
    x0, y0 = coords[0]
    poly = Polygon(Vertex(x0, y0))
    for x, y in coords[1:]:
        poly.insert(Vertex(x, y))
    return poly


def _all_vertices(polygon):
    """Traverse all vertices in the polygon's circular linked list."""
    vertices = []
    current = polygon._v
    for _ in range(polygon.size()):
        vertices.append(current)
        current = current.next
    return vertices


class TestLeastVertexProperties:
    """Property-based tests for leastVertex using Hypothesis."""

    # Feature: least-vertex-in-polygon, Property 1: Result is lexicographically minimal
    @given(
        coords=st.lists(
            st.tuples(
                st.floats(allow_nan=False, allow_infinity=False),
                st.floats(allow_nan=False, allow_infinity=False),
            ),
            min_size=1,
        )
    )
    def test_property1_result_is_lexicographically_minimal(self, coords):
        """
        **Validates: Requirements 1.1, 1.2, 4.2**

        For any non-empty polygon, leastVertex returns a vertex whose (x, y)
        is <= every other vertex's (x, y) under lexicographic order.
        """
        # Feature: least-vertex-in-polygon, Property 1: Result is lexicographically minimal
        poly = _build_polygon_from_coords(coords)
        result = leastVertex(poly)
        for v in _all_vertices(poly):
            assert (result.x, result.y) <= (v.x, v.y)

    # Feature: least-vertex-in-polygon, Property 2: Polygon state is preserved after call
    @given(
        coords=st.lists(
            st.tuples(
                st.floats(allow_nan=False, allow_infinity=False),
                st.floats(allow_nan=False, allow_infinity=False),
            ),
            min_size=1,
        )
    )
    def test_property2_polygon_state_preserved(self, coords):
        """
        **Validates: Requirements 1.4, 3.1, 3.2**

        After a valid call and after a call with a non-callable comparator,
        polygon._v and polygon.size() are unchanged.
        """
        # Feature: least-vertex-in-polygon, Property 2: Polygon state is preserved after call
        poly = _build_polygon_from_coords(coords)
        original_v = poly._v
        original_size = poly.size()

        # Valid call
        leastVertex(poly)
        assert poly._v is original_v
        assert poly.size() == original_size

        # Invalid call with non-callable comparator (integer 42)
        with pytest.raises(TypeError):
            leastVertex(poly, comparator=42)
        assert poly._v is original_v
        assert poly.size() == original_size

    # Feature: least-vertex-in-polygon, Property 3: Non-callable comparator raises TypeError
    @given(
        coords=st.lists(
            st.tuples(
                st.floats(allow_nan=False, allow_infinity=False),
                st.floats(allow_nan=False, allow_infinity=False),
            ),
            min_size=1,
        ),
        non_callable=st.one_of(
            st.integers(),
            st.text(),
            st.lists(st.integers()),
            st.dictionaries(st.text(), st.integers()),
            st.booleans(),
        ),
    )
    def test_property3_non_callable_comparator_raises_type_error(self, coords, non_callable):
        """
        **Validates: Requirements 2.3**

        Any non-callable value passed as comparator must raise TypeError.
        """
        # Feature: least-vertex-in-polygon, Property 3: Non-callable comparator raises TypeError
        poly = _build_polygon_from_coords(coords)
        with pytest.raises(TypeError):
            leastVertex(poly, comparator=non_callable)

    # Feature: least-vertex-in-polygon, Property 4: Result is minimal under custom comparator
    @given(
        coords=st.lists(
            st.tuples(
                st.floats(allow_nan=False, allow_infinity=False),
                st.floats(allow_nan=False, allow_infinity=False),
            ),
            min_size=1,
        )
    )
    def test_property4_result_minimal_under_custom_comparator(self, coords):
        """
        **Validates: Requirements 5.1, 5.2, 5.4**

        With a y-first comparator, the result is not beaten by any other vertex.
        """
        # Feature: least-vertex-in-polygon, Property 4: Result is minimal under custom comparator
        y_first = lambda a, b: (a.y, a.x) < (b.y, b.x)
        poly = _build_polygon_from_coords(coords)
        result = leastVertex(poly, y_first)
        for u in _all_vertices(poly):
            assert not y_first(u, result)

    # Feature: least-vertex-in-polygon, Property 5: Idempotence — repeated calls return the same coordinates
    @given(
        coords=st.lists(
            st.tuples(
                st.floats(allow_nan=False, allow_infinity=False),
                st.floats(allow_nan=False, allow_infinity=False),
            ),
            min_size=1,
        )
    )
    def test_property5_idempotence(self, coords):
        """
        **Validates: Requirements 6.1**

        Calling leastVertex twice on the same polygon returns the same (x, y).
        """
        # Feature: least-vertex-in-polygon, Property 5: Idempotence — repeated calls return the same coordinates
        poly = _build_polygon_from_coords(coords)
        result1 = leastVertex(poly)
        result2 = leastVertex(poly)
        assert (result1.x, result1.y) == (result2.x, result2.y)

    # Feature: least-vertex-in-polygon, Property 6: Order-independence — insertion order does not affect result
    @given(
        coords=st.lists(
            st.tuples(
                st.floats(allow_nan=False, allow_infinity=False),
                st.floats(allow_nan=False, allow_infinity=False),
            ),
            min_size=1,
        )
    )
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property6_order_independence(self, coords):
        """
        **Validates: Requirements 6.2**

        Inserting points in a different order produces the same leastVertex result.
        """
        # Feature: least-vertex-in-polygon, Property 6: Order-independence — insertion order does not affect result
        shuffled = random.sample(coords, len(coords))
        poly1 = _build_polygon_from_coords(coords)
        poly2 = _build_polygon_from_coords(shuffled)
        result1 = leastVertex(poly1)
        result2 = leastVertex(poly2)
        assert (result1.x, result1.y) == (result2.x, result2.y)

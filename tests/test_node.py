"""Unit tests for the Node class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import math
import pytest
from src.core.node import Node

class TestNode:
    """Test cases for Node class."""

    def test_init_default(self):
        """Test default initialization."""
        n = Node()
        assert n.next == n
        assert n.prev == n

    @pytest.fixture
    def sample_nodes(self) -> tuple[Node, Node, Node]:
        """Fixture to create a sample node list."""
        n1 = Node()
        n2 = Node()
        n3 = Node()
        n1.insert(n2)
        n2.insert(n3)
        return n1, n2, n3
    
    def test_navigation(self, sample_nodes):
        """Test navigation through the list."""
        n1, n2, n3 = sample_nodes

        assert n1.next == n2
        assert n2.next == n3
        assert n3.next == n1

        assert n1.prev == n3
        assert n2.prev == n1
        assert n3.prev == n2

    def test_insert(self, sample_nodes):
        """Test insert method."""
        n1, n2, n3 = sample_nodes
        n4 = Node()
        n2.insert(n4)
        assert n2.next == n4
        assert n4.prev == n2
        assert n4.next == n3
        assert n3.prev == n4

    def test_insert_two_nodes(self):
        """Test inserting two nodes in sequence."""
        a = Node()
        b = Node()

        a.insert(b)

        # forward links
        assert a.next is b
        assert b.next is a

        # backward links
        assert a.prev is b
        assert b.prev is a

    def test_remove(self, sample_nodes):
        """Test remove method."""
        n1, n2, n3 = sample_nodes
        n2.remove()
        assert n1.next == n3
        assert n3.prev == n1
        assert n2.next == n2
        assert n2.prev == n2

    def test_splice(self, sample_nodes):
        """Test splice method."""
        n1, n2, n3 = sample_nodes
        n4 = Node()
        n5 = Node()
        n3.insert(n4)
        n4.insert(n5)

        n1.splice(n3)

        assert n1.next == n4
        assert n3.prev == n2
        assert n5.next == n1
        assert n2.prev == n3

    def test_splice_invariant(self):
        """Test that splice maintains list invariants."""

        a = Node()
        b = Node()
        c = Node()
        d = Node()

        a.insert(b)
        b.insert(c)
        c.insert(d)

        # splice c after a
        a.splice(c)

        # invariant check
        start = a
        current = start

        for _ in range(4):
            assert current.next.prev is current
            assert current.prev.next is current
            current = current.next
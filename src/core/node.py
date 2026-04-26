"""Core Node implementation for circular doubly-linked list."""

from typing import Optional


class Node:
    """A node in a circular doubly-linked list.

    This class implements the core node functionality with proper encapsulation
    and following SOLID principles.
    """

    def __init__(self) -> None:
        """Initialize a new node with self-referencing pointers."""
        self.next: Node = self
        self.prev: Node = self

    def insert(self, node: Optional['Node']) -> 'Node':
        """Insert a node after this node.

        Args:
            node: The node to insert. Must not be None or self.

        Returns:
            The inserted node, or self if insertion failed.
        """
        if node is None or node is self:
            return self

        node.prev = self
        node.next = self.next
        self.next.prev = node
        self.next = node
        return node

    def remove(self) -> 'Node':
        """Remove this node from the list.

        Returns:
            The removed node (self).
        """
        if self.next is self and self.prev is self:
            return self

        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = self
        self.prev = self
        return self

    def splice(self, node: Optional['Node']) -> None:
        """Splice a sequence of nodes after this node.

        This inserts the circular sequence whose tail is ``node`` (its head is
        ``node.next``) immediately after this node. The operation either combines
        two lists (inserting the sequence here) or splits a list into two.

        If ``node`` is ``None`` or ``node is self``, the list is unchanged.

        Args:
            node: Tail of the sequence to splice (or None).

        Complexity: O(1).
        """
        if node is None or node is self:
            return

        an = self.next
        bn = node.next

        self.next = bn
        bn.prev = self

        node.next = an
        an.prev = node
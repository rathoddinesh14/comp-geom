"""List operations for circular doubly-linked lists."""

from typing import List, Optional

from .node import Node


def traverse(root: Optional[Node]) -> List[Node]:
    """Traverse a circular linked list starting from root.

    Args:
        root: The starting node for traversal.

    Returns:
        A list of nodes in traversal order.
    """
    nodes: List[Node] = []
    if not root:
        return nodes

    current = root
    while True:
        nodes.append(current)
        current = current.next
        if current == root:
            break
    return nodes
"""Basic usage example for the circular linked list."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.node import Node


def basic_example():
    """Demonstrate basic linked list operations."""
    # Create nodes
    root = Node()
    node_a = Node()
    node_b = Node()

    # Create labels
    labels = {
        root: "Root",
        node_a: "A",
        node_b: "B"
    }

    # Initial state
    from src.core.list_operations import traverse
    print("Initial state:", [labels.get(n, '?') for n in traverse(root)])

    # Insert operations
    root.insert(node_a)
    node_a.insert(node_b)
    print("After insertions:", [labels.get(n, '?') for n in traverse(root)])

    # Remove operation
    node_a.remove()
    print("After removal:", [labels.get(n, '?') for n in traverse(root)])

    print("Basic example completed.")


if __name__ == "__main__":
    basic_example()
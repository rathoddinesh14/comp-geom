"""Main demonstration script for circular linked list (visualization removed)."""

from src.core.node import Node
from src.core.list_operations import traverse


def main():
    """Demonstrate linked list operations via console output."""
    # Initialize nodes
    root = Node()
    a = Node()
    b = Node()
    c = Node()
    other1 = Node()
    other2 = Node()

    labels = {
        root: "root",
        a: "A",
        b: "B",
        c: "C",
        other1: "D",
        other2: "E"
    }


    # Initial state
    print("Initial list:", [labels.get(n, '?') for n in traverse(root)])

    # Insert operations
    root.insert(a)
    a.insert(b)
    b.insert(c)
    print("After insert():", [labels.get(n, '?') for n in traverse(root)])

    print(f"root.next = {labels[root.next]}")
    print(f"root.prev = {labels[root.prev]}")

    # Remove operation
    b.remove()
    print("After remove():", [labels.get(n, '?') for n in traverse(root)])

    # Splice operation
    other1.insert(other2)
    c.splice(other1)
    print("After splice():", [labels.get(n, '?') for n in traverse(root)])

    print("Demo complete (visualization removed).")


if __name__ == "__main__":
    main()
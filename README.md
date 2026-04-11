# Computational Geometry Framework

This Python project provides a framework for implementing computational geometry algorithms and data structures, following SOLID principles and best coding practices. The current implementation demonstrates circular doubly-linked list operations as an example of geometric data structure manipulation with visualization capabilities.

## Features

- **SOLID Principles**: Each component follows single responsibility and dependency inversion
- **Modular Architecture**: Separated core logic and visualization layers
- **Comprehensive Testing**: Unit and integration tests with high coverage

## Project Structure

```
computational-geometry/
├── src/
│   ├── core/                 # Core data structures (currently linked list)
│   └── visualization/        # (removed)
├── tests/                    # Comprehensive test suite
├── docs/                     # Documentation
├── examples/                 # Usage examples
├── AGENT_INSTRUCTIONS.md     # Development guidelines for computational geometry
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## Current Implementation: Linked List Data Structure

The project currently implements a circular doubly-linked list with visualization, serving as an example of geometric data structure manipulation.

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Demo
```bash
python main.py
```

### Computational Geometry Example
```bash
python examples/computational_geometry_demo.py
```

This demonstrates extending the framework to handle geometric primitives, convex hull computation, and polygon visualization.

### As a Package
```python
from src.core.node import Node
from src.core.list_operations import traverse

# Create and manipulate nodes
root = Node()
node = Node()
root.insert(node)

# Inspect list
print([id(n) for n in traverse(root)])
```

## Development

See [AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md) for comprehensive development guidelines.

### Running Tests
```bash
pytest
```

### Code Quality
```bash
black src/
flake8 src/
mypy src/
```

## SOLID Principles Implementation

- **SRP**: Each module has a single responsibility
- **OCP**: Plotter interface allows extension without modification
- **LSP**: All plotter implementations are interchangeable
- **ISP**: Separate interfaces for different concerns
- **DIP**: High-level modules depend on abstractions

## Extending to Computational Geometry

The framework is designed to be extended with additional computational geometry concepts:

### Geometric Primitives
```python
# Future: src/geometry/primitives/point.py
class Point:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
```

### Algorithms
```python
# Future: src/algorithms/convex_hull/graham_scan.py
class GrahamScan:
    def compute(self, points: List[Point]) -> Polygon:
        # Implementation of convex hull algorithm
        pass
```

### Spatial Data Structures
```python
# Future: src/algorithms/spatial/quadtree.py
class QuadTree:
    def __init__(self, boundary: Rectangle):
        self.boundary = boundary
        # Implementation for spatial indexing
```

## Contributing

1. Follow the development guidelines in `AGENT_INSTRUCTIONS.md`
2. Write tests for new functionality
3. Ensure code passes all quality checks
4. Update documentation as needed
5. Consider the broader computational geometry context
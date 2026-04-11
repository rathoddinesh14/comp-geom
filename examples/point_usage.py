"""Basic usage example for the circular linked list."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.point import Point

p1 = Point(1, 0)
p2 = Point(0, 1)

print("p1:", p1)
print("p2:", p2)
print("p1 + p2:", p1 + p2)
print("p1 - p2:", p1 - p2)
print("p1 * 2:", p1 * 2)
print("2 * p2:", 2 * p2)

print("p1[0]:", p1[0])
print("p1[1]:", p1[1])
print("p1 == p2:", p1 == p2)
print("p1 != p2:", p1 != p2)
print("p1 < p2:", p1 < p2)
print("p1 > p2:", p1 > p2)

print("p1 length:", p1.length())
print("p2 length:", p2.length())

print("p1 classify p2 relative to origin:", p2.classify(Point(0, 0), p1))
print("p2 right:", p2.classify(p1, Point(0, 0)))
print("p1 beyond:", p1.classify(Point(0, 0), Point(0.5, 0)))
print("p1 behind:", p1.classify(Point(1.1, 0), Point(2, 0)))
print("p1 between:", p1.classify(Point(0, 0), Point(2, 0)))
print("p1 origin:", p1.classify(Point(1, 0), Point(2, 0)))
print("p1 destination:", p1.classify(Point(0, 0), Point(1, 0)))

print('polar angle of (1, 1):', Point(1, 1).polar_angle())
print('polar angle of (-1, 1):', Point(-1, 1).polar_angle())
print('polar angle of (-1, -1):', Point(-1, -1).polar_angle())
print('polar angle of (1, -1):', Point(1, -1).polar_angle())

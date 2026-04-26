from enum import Enum

class Point_Position(Enum):
    LEFT = 0
    RIGHT = 1
    BEYOND = 2
    BEHIND = 3
    BETWEEN = 4
    ORIGIN = 5
    DESTINATION = 6
    INSIDE = 7
    OUTSIDE = 8
    BOUNDARY = 9

class Point3D_Position(Enum):
    POSITIVE = 0
    NEGATIVE = 1
    ON = 2
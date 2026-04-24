from enum import Enum

class Intersection_Type(Enum):
    COLLINEAR = 0
    PARALLEL = 1
    SKEW = 2
    SKEW_CROSS = 3
    SKEW_NO_CROSS = 4
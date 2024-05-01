from point import Point

from typing import Literal
from enum import Enum
import sys
import math as m

epsilon:float = sys.float_info.epsilon

class Side(Enum):
        LEFT = 0
        BOTTOM = 1
        RIGHT = 2
        TOP = 3
        NIL = 10

TOP: Literal[Side.TOP] = Side.TOP
BOTTOM: Literal[Side.BOTTOM] = Side.BOTTOM
LEFT: Literal[Side.LEFT] = Side.LEFT
RIGHT: Literal[Side.RIGHT] = Side.RIGHT
NIL: Literal[Side.NIL] = Side.NIL

class Intersection:
    def __init__(self, side=None, point=Point()):
        self.side:Side = side or NIL
        self.point:Point = point

class Box:

    def __init__(self, left=0.0, bottom=0.0, right=0.0, top=0.0):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def contains(self, point:Point):
         return (point.x >= self.left - epsilon and
                 point.x <= self.right + epsilon and
                 point.y >= self.bottom - epsilon and
                 point.y <= self.top + epsilon)
    
    def get_first_intersection(self, origin:Point, dir:Point):
        intersection:Intersection = Intersection()

        t:float = m.inf
        if dir.x > 0.0:
            t = (self.right - origin.x) / dir.x
            intersection.side = RIGHT
            intersection.point = origin + t * dir
        elif dir.x < 0.0:
            t = (self.left - origin.x) /dir.x
            intersection.side = LEFT
            intersection.point = origin + t * dir
        
        if dir.y > 0.0:
            new_t = (self.top - origin.y) / dir.y
            if (new_t < t):
                intersection.side = TOP
                intersection.point = origin + new_t * dir
        elif dir.y < 0.0:
            new_t = (self.bottom - origin.y) / dir.y
            if new_t < t:
                intersection.side = BOTTOM
                intersection.point = origin + new_t * dir
        
        return intersection
    
    def get_intersections(self, origin:Point, dest:Point, intersections_list:list[Intersection]):
        dir:Point = dest - origin

        t:list[float] = [0.0, 0.0]
        i:int = 0

        # left
        if (origin.x < self.left - epsilon) or (dest.x < (self.left - epsilon)):
            t[i] = (self.left - origin.x) / dir.x
            if t[i] > epsilon and t[i] < (1.0 - epsilon):
                intersections_list[i].side = LEFT
                intersections_list[i].point = origin + t[i] * dir
                if (intersections_list[i].point.y >= (self.bottom - epsilon) and
                    intersections_list[i].point.y <= (self.top + epsilon)):
                    i += 1

        # right
        if (origin.x > (self.right + epsilon)) or (dest.x > (self.right + epsilon)):
            t[i] = (self.right - origin.x) / dir.x
            if t[i] > epsilon and t[i] < (1.0 - epsilon):
                intersections_list[i].side = RIGHT
                intersections_list[i].point = origin + t[i] * dir
                if (intersections_list[i].point.y >= (self.bottom - epsilon) and
                    intersections_list[i].point.y <= (self.top + epsilon)):
                    i += 1

        # bottom
        if (origin.y < self.bottom - epsilon) or (dest.y < (self.bottom - epsilon)):
            t[i] = (self.bottom - origin.y) / dir.y
            if i < 2 and t[i] > epsilon and t[i] < (1.0 - epsilon):
                intersections_list[i].side = BOTTOM
                intersections_list[i].point = origin + t[i] * dir
                if (intersections_list[i].point.x >= (self.left - epsilon) and
                    intersections_list[i].point.x <= (self.right + epsilon)):
                    i += 1

        # top
        if (origin.y > self.top + epsilon) or (dest.y > (self.top + epsilon)):
            t[i] = (self.top - origin.y) / dir.y
            if i < 2 and t[i] > epsilon and t[i] < (1.0 - epsilon):
                intersections_list[i].side = TOP
                intersections_list[i].point = origin + t[i] * dir
                if (intersections_list[i].point.x >= (self.left - epsilon) and
                    intersections_list[i].point.x <= (self.right + epsilon)):
                    i += 1

        if i == 2 and t[0] > t[1]:
            intersections_list[0], intersections_list[1] = intersections_list[1], intersections_list[0]
        return i
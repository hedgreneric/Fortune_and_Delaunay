import fortune
import dcel
from point import Point

from enum import Enum
import math

class Color(Enum):
    RED = 1
    BLACK = 2

class Arc:
    def __init__(self, color=None, parent=None, left=None, right=None, site=None, left_half_edge=None,
                 right_half_edge=None, event=None, prev=None, next=None ):
        # used for balancing
        self.color = color

        # hierarchy
        self.parent = parent # Arc
        self.left = left # Arc
        self.right = right # Arc

        # diagram
        self.site = site # dcel.site
        self.left_half_edge = left_half_edge # dcel.half_edge
        self.right_half_edge = right_half_edge # dcel.half_edge
        self.event = event # Event

        self.prev = prev # Arc
        self.next = next # Arc

class BeachLine:
    def __init__(self):
        self.nil = None # Arc
        self.root = None # Arc
        self.beach_line_y = 0.0

    def is_empty(self):
        return self.root == None
    
    def set_root(self, arc:Arc):
        self.root = arc
        self.root = Color.BLACK

    def create_arc(site:dcel.Site):
        return Arc(color=Color.RED, site=site)
    
    def is_none(arc:Arc):
        return arc is None
    
    def compute_breakpoint(pt1:Point, pt2:Point, l:float):
        x1 = float(pt1.x)
        y1 = float(pt1.y)
        x2 = float(pt2.x)
        y2 = float(pt2.y)

        d1 = 1.0 / (2.0 * (y1 - l))
        d2 = 1.0 / (2.0 * (y2 - l))
        a = d1 - d2
        b = 2.0 * ((x2 * d2) - (x1 * d1))
        c = (((y1**2) + (x1**2) - (l**2)) * d1) - (((y2**2) + (x2**2) - (l**2)) * d2)
        delta = b * b - 4.0 * a * c

        return (-b + math.sqrt(delta)) / (2.0 * a)

    
    def get_arc_above(self, point:Point, l:float):
        node = self.root
        found = False
        while not found:
            breakpoint_left = float('-inf')
            breakpoint_right = float('inf')
            if not self.is_none(node.prev):
                breakpoint_left = self.compute_breakpoint(node.prev.site.point, node.site.point, l)

            if not self.is_none(node.next):
                breakpoint_right = self.compute_breakpoint(node.site.point, node.next.site.point, l)
            
            if point.x < breakpoint_left:
                node = node.left
            elif point.x > breakpoint_right:
                node = node.right
            else:
                found = True

        return node





    # def insert_before(curr:Arc, insert:Arc):
    #     if curr.left is None:
    #         curr.left = insert
    #     else:
    #         curr.prev.right = insert
    #         insert.parent = curr.prev

    #     insert.prev = curr.prev
    #     if insert.prev is not None:
    #         insert.prev.next = insert
    #     insert.next = curr
    #     curr.prev = insert

        # insertFixup(insert)
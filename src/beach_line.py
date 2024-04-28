import fortune as f
import dcel as DCEL
from point import Point

from enum import Enum
import math as m
from typing import Literal

class Color(Enum):
    RED = 1
    BLACK = 2

RED: Literal[Color.RED] = Color.RED
BLACK: Literal[Color.RED] = Color.BLACK

class Arc:
    def __init__(self, color=None, parent=None, left=None, right=None, site=None, left_half_edge=None,
                 right_half_edge=None, event=None, prev=None, next=None ):
        # used for balancing
        self.color:Color = color

        # hierarchy
        self.parent:Arc = parent # Arc
        self.left:Arc = left # Arc
        self.right:Arc = right # Arc

        # diagram
        self.site:DCEL.Site = site # dcel.site
        self.left_half_edge:DCEL.Half_Edge = left_half_edge # dcel.half_edge
        self.right_half_edge:DCEL.Half_Edge = right_half_edge # dcel.half_edge
        self.event:f.Event = event # Event

        self.prev:Arc = prev # Arc
        self.next:Arc = next # Arc

class BeachLine:
    def __init__(self):
        self.null:Arc = Arc(color=BLACK)
        self.root:Arc = self.null
        self.beach_line_y:float = 0.0

    def is_empty(self):
        return self.is_none(self.root)
    
    def set_root(self, arc:Arc):
        self.root = arc
        self.root.color = BLACK

    def create_arc(self, site:DCEL.Site):
        null = self.null
        return Arc(Color.RED, null, null, null, site, None, None, None, null, null)
    
    def is_none(self, arc:Arc):
        return arc is self.null
    
    def compute_breakpoint(self, pt1:Point, pt2:Point, l:float):
        x1 = pt1.x
        y1 = pt1.y
        x2 = pt2.x
        y2 = pt2.y

        d1 = 1.0 / (2.0 * (y1 - l))
        d2 = 1.0 / (2.0 * (y2 - l))
        a = d1 - d2
        b = 2.0 * ((x2 * d2) - (x1 * d1))
        c = (((y1**2) + (x1**2) - (l**2)) * d1) - (((y2**2) + (x2**2) - (l**2)) * d2)
        delta = b * b - 4.0 * a * c

        return (-b + m.sqrt(delta)) / (2.0 * a)

    
    def get_arc_above(self, point:Point, l:float):
        node = self.root
        found = False
        while not found:
            breakpoint_left = float(m.inf)
            breakpoint_right = float(-m.inf)
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
    
    def replace(self, a:Arc, b:Arc):
        self.replace_node(a, b)
        b.left = a.left
        b.right = a.right
        if (not self.is_none(b.left)):
            b.left.parent = b
        if (not self.is_none(b.right)):
            b.right.parent = b
        b.prev = a.prev
        b.next = a.next
        if (not self.is_none(b.prev)):
            b.prev.next = b
        if (not self.is_none(b.next)):
            b.next.prev = b
        b.color = a.color
    
    def replace_node(self, a:Arc, b:Arc):
        if self.is_none(a.parent):
            self.root = b
        elif a is a.parent.left:
            a.parent.left = b
        else:
            a.parent.right = b

        b.parent = a.parent

    def insert_before(self, a:Arc, b:Arc):
        if self.is_none(a.left):
            a.left = b
            b.parent = a
        else:
            a.prev.right = b
            b.parent = a.prev

        b.prev = a.prev
        if not self.is_none(b.prev):
            b.prev.next = b
        b.next = a
        a.prev = b

        self.insert_fixup(b)

    def insert_after(self, a:Arc, b:Arc):
        if self.is_none(a.right):
            a.right = b
            b.parent = a
        else:
            a.next.left = b
            b.parent = a.next
        
        b.next = a.next
        if not self.is_none(b.next):
            b.next.prev = b
        b.prev = a
        a.next = b

        self.insert_fixup(b)
        
    def insert_fixup(self, a:Arc):
        g:Arc

        while a.parent.color == RED:
            if a.parent is a.parent.parent.left:
                g = a.parent.parent.right

                if g.color == RED:
                    a.parent.color = BLACK
                    g.color = BLACK
                    a.parent.parent.color = RED
                    a = a.parent.parent
                else:
                    if a is a.parent.right:
                        a = a.parent
                        self.rotate_left(a)
                    a.parent.color = BLACK
                    a.parent.parent.color = RED
                    self.rotate_right(a.parent.parent)
            else:
                g = a.parent.parent.left

                if g.color == RED:
                    a.parent.color = BLACK
                    g.color = BLACK
                    a.parent.parent.color = RED
                    a = a.parent.parent
                else:
                    if a is a.parent.left:
                        a = a.parent
                        self.rotate_right(a)
                    a.parent.color = BLACK
                    a.parent.parent.color = RED
                    self.rotate_left(a.parent.parent)
        
        self.root.color = BLACK

    def remove_fixup(self, a:Arc):
        u:Arc

        while a is not self.root and a.color == BLACK:
            if a is a.parent.left:
                u = a.parent.right

                if u.color == RED:
                    u.color = BLACK
                    a.parent.color = RED
                    self.rotate_left(a.parent)
                    u = a.parent.right

                if u.left.color == BLACK and u.right.color == BLACK:
                    u.color = RED
                    a = a.parent
                else:
                    if u.right.color == BLACK:
                        u.left.color = BLACK
                        u.color = RED
                        self.rotate_right(u)
                        u = a.parent.right
                    
                    u.color = a.parent.color
                    a.parent.color = BLACK
                    u.right.color = BLACK
                    self.rotate_left(a.parent)
                    a = self.root
            else:
                u = a.parent.left
                
                if u.color == RED:
                    u.color = BLACK
                    a.parent.color = RED
                    self.rotate_right(a.parent)
                    u = a.parent.left
                
                if u.left.color == BLACK and u.right.color == BLACK:
                    u.color = RED
                    a = a.parent
                else:
                    if u.left.color == BLACK:
                        u.right.color = BLACK
                        u.color = RED
                        self.rotate_left(u)
                        u = a.parent.left
                    
                    u.color = a.parent.color
                    a.parent.color = BLACK
                    u.left.color = BLACK
                    self.rotate_right(a.parent)
                    a = self.root

        a.color = BLACK

    def rotate_left(self, a:Arc):
        b = a.right
        a.right = b.left
        if not self.is_none(b.left):
            b.left.parent = a
        b.parent = a.parent
        if self.is_none(a.parent):
            self.root = b
        elif a.parent.left is a:
            a.parent.left = b
        else:
            a.parent.right = b
        
        b.left = a
        a.parent = b

    def rotate_right(self, a:Arc):
        b = a.left
        a.left = b.right
        if not self.is_none(b.right):
            b.right.parent = a
        b.parent = a.parent
        if self.is_none(a.parent):
            self.root = b
        elif a.parent.left is a:
            a.parent.left = b
        else:
            a.parent.right = b

        b.right = a
        a.parent = b


    def remove(self, a:Arc):
        n:Arc
        u:Arc = a
        u_init_color:Color = u.color

        if self.is_none(a.left):
            n = a.right
            self.replace_node(a, a.right)
        elif self.is_none(a.right):
            n = a.left
            self.replace_node(a, a.left)
        else:
            u = self.least(a.right)
            u_init_color = u.color
            n = u.right
            if u.parent is a:
                n.parent = u
            else:
                self.replace_node(u, u.right)
                u.right = a.right
                u.right.parent = u
            
            self.replace_node(a, u)
            u.left = a.left
            u.left.parent = u
            u.color = a.color

        if u_init_color == BLACK:
            self.remove_fixup(n)
        
        if not self.is_none(a.prev):
            a.prev.next = a.next
        
        if not self.is_none(a.next):
            a.next.prev = a.prev
    
    def least(self, a:Arc):
        while not self.is_none(a.left):
            a = a.left
        return a
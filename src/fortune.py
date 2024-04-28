import dcel as DCEL
from main import voronoi_dcel
from point import Point
import beach_line as BL
from priority_queue import IndexedSortedList

import heapq
# from sortedcontainers import SortedList
from enum import Enum

bl = BL.BeachLine()
event_queue = IndexedSortedList(key=lambda e: (-e.point.y, e.point.x))

dcel = voronoi_dcel

class Type(Enum):
    SITE = 1
    CIRCLE = 2


class Event:
    def __init__(self, site:DCEL.Site=None):
        self.point:Point = site.point
        self.valid:bool = True
        self.site:DCEL.Site = site
        self.index:int = -1
        if site is None:
            self.type:Type = Type.CIRCLE
        else:
            self.type:Type = Type.SITE

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], DCEL.Site):
            # Initialization for SITE events
            self.site:DCEL.Site = args[0]
            self.y = self.point.y
            self.index:int = -1
            self.type:Type = Type.SITE

        elif len(args) == 3:
            # Initialization for CIRCLE events
            y, point, arc = args
            self.type = Type.CIRCLE
            self.y = y
            self.index = -1
            self.point = point
            self.arc = arc
        else:
            raise ValueError("Invalid arguments for Event initialization")


def fortune_algorithm():
    """
    add a site event in the event queue for each site
    while the event queue is not empty
        pop the top event
        if the event is a site event
            insert a new arc in the beachline
            check for new circle events
        else
            create a vertex in the diagram
            remove the shrunk arc from the beachline
            delete invalidated events
            check for new circle events
    """

    for site in dcel.sites_list:
        event_queue.add(Event(site))

    while len(event_queue) != 0:
        e = event_queue.pop(0)
        bl.beach_line_y = e.point.y
        if e.type is Type.SITE:
            handle_site_event(e)
        else: 
            handle_circle_event(e)


def handle_site_event(event):
    site = event.site

    # check if the beachline is empty
    if bl.isEmpty():
        bl.setRoot(bl.create_arc(site))

    # look for the arc above the site
    arc_to_break = bl.get_arc_above(site.point, bl.beach_line_y)
    delete_event(arc_to_break)

    # replace this arc with the new arcs
    middle_arc = break_arc(arc_to_break, site)
    left_arc = middle_arc.prev
    right_arc = middle_arc.next

    # add edge to dcel
    add_edge(left_arc, right_arc)
    middle_arc.right_half_edge = middle_arc.left_half_edge
    right_arc.leftHalfEdge = left_arc.right_half_edge

    # check circle events
    if not bl.is_none(left_arc.prev):
        add_event(left_arc.prev, left_arc, middle_arc)
    if not bl.is_none(right_arc.prev):
        add_event(middle_arc, right_arc, right_arc.next)
    

def handle_circle_event(gamma):
    print()


def delete_event(arc:BL.Arc):
    if arc.event is not None:
        event_queue.pop(arc.event.index)
        arc.event = None

def break_arc(arc:BL.Arc, site:DCEL.Site):
    middle_arc = bl.create_arc(site)

    left_arc = bl.create_arc(arc.site)
    left_arc.left_half_edge = arc.left_half_edge

    right_arc = bl.create_arc(arc.site)
    right_arc.right_half_edge = arc.right_half_edge

    bl.replace(arc, middle_arc)
    bl.insert_before(middle_arc, left_arc)
    bl.insert_after(middle_arc, right_arc)

    del arc

    return middle_arc


def add_edge(left:BL.Arc, right:BL.Arc):
    left.right_half_edge = dcel.create_half_edge(left.site.face)
    right.left_half_edge = dcel.create_half_edge(right.site.face) # FIX constructor

    left.right_half_edge.twin = right.left_half_edge
    right.left_half_edge.twin = left.right_half_edge


def add_event(left:BL.Arc, middle:BL, right:BL.Arc):
    y = 0.0
    converge_point = get_convergence_point(left.site.point, middle.site.point, right.site.point)
    is_below = y <= bl.beach_line_y
    is_left_breakpoint_moving_right = is_moving_right(left, middle)
    is_right_breakpoint_moving_right = is_moving_right(middle, right)
    left_init_x = get_init_x(left, middle, is_left_breakpoint_moving_right)
    right_init_x = get_init_x(middle, right, is_right_breakpoint_moving_right)

    is_valid:bool = ((is_left_breakpoint_moving_right and left_init_x < converge_point.x) or (not is_left_breakpoint_moving_right and left_init_x > converge_point.x)) and ((is_right_breakpoint_moving_right and right_init_x < converge_point.x) or (not is_right_breakpoint_moving_right and right_init_x > converge_point.x))
    
    if is_valid and is_below:
        event:Event = Event()

def get_convergence_point(pt1:Point, pt2:Point, pt3:Point, y:float):
    print()


def is_moving_right(left:BL.Arc, right:BL.Arc):
    return left.site.point.y < right.site.point.y


def get_init_x(left:BL.Arc, right:BL.Arc, is_moving_right:bool):
    return left.site.point.x if is_moving_right else right.site.point.x


def set_origin(left:BL.Arc, right:BL.Arc, vertex:DCEL.Vertex):
    left.right_half_edge.origin = vertex
    right.left_half_edge.destination = vertex
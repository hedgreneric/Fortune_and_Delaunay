import dcel as DCEL
from point import Point
import beach_line as BL
from priority_queue import IndexedSortedList

from main import voronoi_dcel

import heapq
# from sortedcontainers import SortedList
from enum import Enum

bl = BL.BeachLine()
event_queue = IndexedSortedList(key=lambda e: (-e.point.y, e.point.x))

class Type(Enum):
    SITE = 1
    CIRCLE = 2


class Event:
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], DCEL.Site):
            # Initialization for SITE events
            self.site:DCEL.Site = args[0]
            self.point = self.site.point
            self.y:float = self.point.y
            self.index:int = self.site.index
            self.type:Type = Type.SITE

        elif len(args) == 3:
            # Initialization for CIRCLE events
            y, point, arc = args
            self.type:Type = Type.CIRCLE
            self.y:float = y
            self.index:int = -1
            self.point:Point = point
            self.arc:BL.Arc = arc
        else:
            raise ValueError("Invalid arguments for Event initialization")
        
    def __lt__(self, other):
        return self.y < other.y
    
class Voronoi_Diagram:
    def __init__(self, dcel:DCEL.DCEL):
        self.dcel = dcel
        self.fortune_algorithm()


    def fortune_algorithm(self):
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
        if self.dcel is None: raise ValueError("Invalid arguments for Fortune Algorithm")

        for site in self.dcel.sites_list:
            event_queue.add(Event(site))

        while len(event_queue) != 0:
            e = event_queue.pop(0)
            bl.beach_line_y = e.point.y
            if e.type is Type.SITE:
                self.handle_site_event(e)
            else: 
                self.handle_circle_event(e)


    def handle_site_event(self, event:Event):
        site = event.site

        # check if the beachline is empty
        if bl.is_empty():
            bl.set_root(bl.create_arc(site))
            return

        # look for the arc above the site
        arc_to_break = bl.get_arc_above(site.point, bl.beach_line_y)
        self.delete_event(arc_to_break)

        # replace this arc with the new arcs
        middle_arc = self.break_arc(arc_to_break, site)
        left_arc = middle_arc.prev
        right_arc = middle_arc.next

        # add edge to dcel
        self.add_edge(left_arc, middle_arc)
        middle_arc.right_half_edge = middle_arc.left_half_edge
        right_arc.left_half_edge = left_arc.right_half_edge

        # check circle events
        if not bl.is_none(left_arc.prev):
            self.add_event(left_arc.prev, left_arc, middle_arc)
        if not bl.is_none(right_arc.prev):
            self.add_event(middle_arc, right_arc, right_arc.next)


    def handle_circle_event(self, event:Event):
        point:Point = event.point
        arc:BL.Arc = event.arc

        vertex:DCEL.Vertex = self.dcel.create_vertex(point=point)

        # delete all the events with arc
        left_arc:BL.Arc = arc.prev
        right_arc:BL.Arc = arc.next

        self.delete_event(left_arc)
        self.delete_event(right_arc)

        # update beachline and dcel
        self.remove_arc(arc, vertex)

        # add new circle events
        if not bl.is_none(left_arc.prev):
            self.add_event(left_arc.prev, left_arc, right_arc)
        if not bl.is_none(right_arc.next):
            self.add_event(left_arc, right_arc, right_arc.next)


    def remove_arc(self, arc:BL.Arc, vertex:DCEL.Vertex):

        # finish edges
        self.set_destination(arc.prev, arc, vertex)
        self.set_destination(arc, arc.next, vertex)

        # join edges at the middle arc
        arc.left_half_edge.next = arc.right_half_edge
        arc.right_half_edge.prev = arc.left_half_edge

        bl.remove(arc)

        prev_half_edge:DCEL.Half_Edge = arc.prev.right_half_edge
        next_half_edge:DCEL.Half_Edge = arc.next.left_half_edge

        self.add_edge(arc.prev, arc.next)

        self.set_origin(arc.prev, arc.next, vertex)
        self.set_prev_half_edge(arc.prev.right_half_edge, prev_half_edge)
        self.set_prev_half_edge(next_half_edge, arc.next.left_half_edge)

        del arc


    def delete_event(self, arc:BL.Arc):
        if arc.event is not None:
            event_queue.pop(arc.event.index)
            arc.event = None

    def break_arc(self, arc:BL.Arc, site:DCEL.Site):
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


    def add_edge(self, left:BL.Arc, right:BL.Arc):
        left.right_half_edge = self.dcel.create_half_edge(left.site.face)
        right.left_half_edge = self.dcel.create_half_edge(right.site.face)

        left.right_half_edge.twin = right.left_half_edge
        right.left_half_edge.twin = left.right_half_edge


    def add_event(self, left:BL.Arc, middle:BL.Arc, right:BL.Arc):
        y:float

        converge_point, y = self.get_convergence_point(left.site.point, middle.site.point, right.site.point)
        is_below = y <= bl.beach_line_y
        is_left_breakpoint_moving_right = self.is_moving_right(left, middle)
        is_right_breakpoint_moving_right = self.is_moving_right(middle, right)
        left_init_x = self.get_init_x(left, middle, is_left_breakpoint_moving_right)
        right_init_x = self.get_init_x(middle, right, is_right_breakpoint_moving_right)

        is_valid:bool = ((is_left_breakpoint_moving_right and left_init_x < converge_point.x) or (not is_left_breakpoint_moving_right and left_init_x > converge_point.x)) and ((is_right_breakpoint_moving_right and right_init_x < converge_point.x) or (not is_right_breakpoint_moving_right and right_init_x > converge_point.x))

        if is_valid and is_below:
            event:Event = Event(y, converge_point, middle)
            middle.event = event
            event_queue.add(event)


    def get_convergence_point(self, pt1:Point, pt2:Point, pt3:Point):
        v1:Point = (pt1 - pt2).get_orthogonal()
        v2:Point = (pt2 - pt3).get_orthogonal()
        delta:Point = 0.5 * (pt3 - pt1)
        t:float = delta.get_det(v2) / v1.get_det(v2)
        center:Point = 0.5 * (pt1 + pt2) + (t * v1)
        radius:float = center.get_distance(pt1)
        y = center.y - radius
        return center, y


    def is_moving_right(self, left:BL.Arc, right:BL.Arc):
        return left.site.point.y < right.site.point.y


    def get_init_x(self, left:BL.Arc, right:BL.Arc, is_moving_right:bool):
        return left.site.point.x if is_moving_right else right.site.point.x


    def set_origin(self, left:BL.Arc, right:BL.Arc, vertex:DCEL.Vertex):
        left.right_half_edge.destination = vertex
        right.left_half_edge.origin = vertex

    def set_destination(self, left:BL.Arc, right:BL.Arc, vertex:DCEL.Vertex):
        left.right_half_edge.origin = vertex
        right.left_half_edge.destination = vertex

    def set_prev_half_edge(self, prev:DCEL.Half_Edge, next:DCEL.Half_Edge):
        prev.next = next
        next.prev = prev
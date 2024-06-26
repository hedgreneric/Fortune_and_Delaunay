import dcel as DCEL
from point import Point
import beach_line as BL
from priority_queue import IndexedSortedList
from box import Box
from box import Intersection
from box import Side


import math as m
from enum import Enum
from typing import List, Dict
import sys

bl = BL.BeachLine()
event_queue = IndexedSortedList(key=lambda e: (-e.point.y, e.point.x))
epsilon:float = sys.float_info.epsilon

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
    
    def __gt__(self, other):
        return self.y > other.y
    
class Linked_Vertex:
    def __init__(self, prev_half_edge = DCEL.Half_Edge(), vertex = DCEL.Vertex(), next_half_edge = DCEL.Half_Edge):
        self.prev_half_edge:DCEL.Half_Edge = prev_half_edge
        self.vertex:DCEL.Vertex = vertex
        self.next_half_edge:DCEL.Half_Edge = next_half_edge
    
class Voronoi_Diagram:
    def __init__(self, dcel:DCEL.DCEL):
        self.dcel = dcel

    def fortune_algorithm(self):
        if self.dcel is None: raise ValueError("Invalid arguments for Fortune Algorithm")

        for site in self.dcel.sites_list:
            event_queue.add(Event(site))

        while len(event_queue) != 0:
            e:Event = event_queue.pop(0)
            bl.beach_line_y = e.y
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
        if not bl.is_none(right_arc.next):
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

        is_valid:bool = (((is_left_breakpoint_moving_right and left_init_x < converge_point.x) or
                          (not is_left_breakpoint_moving_right and left_init_x > converge_point.x)) and
                         ((is_right_breakpoint_moving_right and right_init_x < converge_point.x) or
                          (not is_right_breakpoint_moving_right and right_init_x > converge_point.x)))

        if is_valid and is_below:
            event:Event = Event(y, converge_point, middle)
            middle.event = event
            event_queue.add(event)


    def get_convergence_point(self, pt1:Point, pt2:Point, pt3:Point):
        v1:Point = (pt1 - pt2).get_orthogonal()
        v2:Point = (pt2 - pt3).get_orthogonal()

        if v1.x == v2.x: v1.x += epsilon
        if v1.y == v1.y: v1.y += epsilon
 
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

    def bound_box(self, box:Box):
        for v in self.dcel.vertices_list:
            box.left = min(v.point.x, box.left)
            box.bottom = min(v.point.y, box.bottom)
            box.right = max(v.point.x, box.right)
            box.top = max(v.point.y, box.top)

        linked_vertices_list:list[Linked_Vertex] = []
        vertices_dict = {i: [Linked_Vertex() for _ in range(8)] for i in range(len(self.dcel.sites_list))}

        # get all unbounded half_edges
        if not bl.is_empty():
            left_arc = bl.get_left_most_arc()
            right_arc = left_arc.next

            while not bl.is_none(right_arc):
                dir:Point = (left_arc.site.point - right_arc.site.point).get_orthogonal()
                origin:Point = (left_arc.site.point + right_arc.site.point) * 0.5

                intersection:Intersection = box.get_first_intersection(origin, dir)

                vertex:DCEL.Vertex = self.dcel.create_vertex(intersection.point)
                self.set_destination(left_arc, right_arc, vertex)
                
                if left_arc.site.index in vertices_dict.keys():
                    vertices_dict[left_arc.site.index] = [None] * len(vertices_dict[left_arc.site.index])

                if right_arc.site.index in vertices_dict.keys():
                    vertices_dict[right_arc.site.index] = [None] * len(vertices_dict[right_arc.site.index])

                linked_vertices_list.append(Linked_Vertex(vertex=vertex, next_half_edge=left_arc.right_half_edge))
                vertices_dict[left_arc.site.index][2 * intersection.side.value] = linked_vertices_list[-1]

                linked_vertices_list.append(Linked_Vertex(prev_half_edge=right_arc.left_half_edge, vertex=vertex))
                vertices_dict[right_arc.site.index][2 * intersection.side.value] = linked_vertices_list[-1]

                left_arc = right_arc
                right_arc = right_arc.next
            
        # add corners
        for key, cell_vertices in vertices_dict.items():
            for i in range(5):
                side:Side = Side(i % 4)
                next_side:Side = Side((side.value + 1) % 4)

                if cell_vertices[2 * side.value] is None and cell_vertices[2 * side.value + 1] is None:
                    prev_side = Side((side.value + 3) % 4)
                    corner:DCEL.Vertex = self.dcel.create_corner(box, side)
                    linked_vertices_list.append(Linked_Vertex(vertex=corner))
                    cell_vertices[2 * prev_side.value + 1] = linked_vertices_list[-1]
                    cell_vertices[2 * side.value] = linked_vertices_list[-1]
                elif cell_vertices[2 * side.value] is not None and cell_vertices[2 * side.value + 1] is None:
                    corner:DCEL.Vertex = self.dcel.create_corner(box, next_side)
                    linked_vertices_list.append(Linked_Vertex(vertex=corner))
                    cell_vertices[2 * side.value + 1] = linked_vertices_list[-1]
                    cell_vertices[2 * next_side.value] = linked_vertices_list[-1]
        
        for key, cell_vertices in vertices_dict.items():
            i:int = key
            
            for side_num in range(4):
                if cell_vertices[2 * side.value] is not None:
                    he:DCEL.Half_Edge = self.dcel.create_half_edge(self.dcel.get_face(i))
                    he.origin = cell_vertices[2 * side.value].vertex
                    he.destination = cell_vertices[2 * side.value + 1].vertex
                    cell_vertices[2 * side.value].next_half_edge = he
                    he.prev = cell_vertices[2 * side.value].prev_half_edge
                    if cell_vertices[2 * side.value].prev_half_edge is not None:
                        cell_vertices[2 * side.value].prev_half_edge.next = he
                    cell_vertices[2 * side.value + 1].prev_half_edge = he
                    he.next = cell_vertices[2 * side.value + 1].next_half_edge
                    if cell_vertices[2 * side.value + 1].next_half_edge is not None:
                        cell_vertices[2 * side.value + 1].next_half_edge.prev = he
        
        return True



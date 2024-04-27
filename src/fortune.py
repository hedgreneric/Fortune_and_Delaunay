import dcel
from point import Point
import beach_line
from priority_queue import IndexedSortedList

import heapq
# from sortedcontainers import SortedList
from enum import Enum

bl = beach_line.BeachLine()
event_queue = IndexedSortedList(key=lambda e: (-e.point.y, e.point.x))

class Type(Enum):
    SITE = 1
    CIRCLE = 2

class Event:
    def __init__(self, x:float, y:float, site=None):
        self.point = Point(x, y)
        self.valid = True
        self.site = site
        self.index = -1
        if site is None:
            self.type = Type.CIRCLE
        else:
            self.type = Type.SITE

def fortune_algorithm(dcel):
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
        event_queue.add(Event(site.point.x, site.point.y, site))


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
    middle_arc = 


def handle_circle_event(gamma):
    print()

def delete_event(arc:beach_line.Arc):
    if arc.event is not None:
        event_queue.pop(arc.event.index)
        arc.event = None

def break_arc(arc:beach_line.Arc, site:dcel.Site):
    middle_arc = bl.create_arc(site)

    left_arc = bl.create_arc(arc.site)
    left_arc.left_half_edge = arc.left_half_edge

    right_arc = bl.create_arc(arc.site)
    right_arc.right_half_edge = arc.right_half_edge

    # replace
    # insert before
    # insert after

    del arc

    return middle_arc

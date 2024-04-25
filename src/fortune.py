import heapq
from collections import namedtuple
from math import sqrt

class VoronoiDiagram:
    def __init__(self, points):
        self.sites = points
        self.vertices = []
        self.half_edges = []
        self.faces = []

    def getNbSites(self):
        return len(self.sites)

    def getSite(self, index):
        return self.sites[index]

    def createVertex(self, point):
        vertex = Vertex(point)
        self.vertices.append(vertex)
        return vertex

    def createHalfEdge(self, face):
        half_edge = HalfEdge(face)
        self.half_edges.append(half_edge)
        return half_edge


class Vertex:
    def __init__(self, point):
        self.point = point


class HalfEdge:
    def __init__(self, face):
        self.face = face
        self.origin = None
        self.destination = None
        self.prev = None
        self.next = None
        self.twin = None


class FortuneAlgorithm:
    def __init__(self, points):
        self.diagram = VoronoiDiagram(points)
        self.events = []
        self.beachline = None
        self.beachlineY = None

    def construct(self):
        # Initialize event queue
        for i in range(self.diagram.getNbSites()):
            site = self.diagram.getSite(i)
            heapq.heappush(self.events, (site.y, Event("SITE", site.y, site, site)))

        while self.events:
            _, event = heapq.heappop(self.events)
            self.beachlineY = event.y
            if event.type == "SITE":
                self.handleSiteEvent(event)
            else:
                self.handleCircleEvent(event)

    def handleSiteEvent(self, event):
        site = event.site
        # Check if beachline is empty
        if self.beachline is None:
            self.beachline = Arc(site, None, None, None, None)
            return
        
        # Locate arc to break
        arcToBreak = self.locateArcAbove(site)
        self.deleteEvent(arcToBreak)
        
        # Create the new arcs and add edge
        middleArc = self.breakArc(arcToBreak, site)
        leftArc = middleArc.prev
        rightArc = middleArc.next
        
        # Add edge and check circle events
        self.addEdge(leftArc, middleArc)
        if leftArc.prev:
            self.addEvent(leftArc.prev, leftArc, middleArc)
        if rightArc.next:
            self.addEvent(middleArc, rightArc, rightArc.next)

    def breakArc(self, arc, site):
        # Create new arcs and insert into the beachline
        middleArc = Arc(site, arc, arc.next, None, None)
        leftArc = Arc(arc.site, arc.prev, middleArc, None, None)
        rightArc = Arc(arc.site, middleArc, arc.next, None, None)
        middleArc.prev = leftArc
        middleArc.next = rightArc
        arc.prev = leftArc
        arc.next = rightArc
        self.deleteEvent(arc)
        return middleArc

    def locateArcAbove(self, site):
        # Dummy implementation, proper logic required
        current_arc = self.beachline
        while current_arc:
            # Implement logic to find the correct arc above the site
            current_arc = current_arc.next
        return current_arc

    def deleteEvent(self, arc):
        if arc.event:
            self.events.remove((arc.event.y, arc.event))
            arc.event = None

    def addEvent(self, leftArc, middleArc, rightArc):
        # Logic to add circle event if valid
        pass

    def addEdge(self, leftArc, middleArc):
        # Create and set half edges
        pass


# Example usage
points = [Vector2(1, 1), Vector2(4, 4), Vector2(2, 5), Vector2(6, 3)]
fa = FortuneAlgorithm(points)
fa.construct()


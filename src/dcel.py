import math as m
from point import Point

class Site:
    def __init__(self, point, index):
        self.index = index
        self.point = point
        self.face = None

class Vertex:
    def __init__(self, point, index):
        self.index = index
        self.point = point
        self.incident_edges_list = [] # Incident Edges

class Half_Edge:
    def __init__(self, origin=None, destination=None):
        self.origin = origin
        self.destination = destination
        self.prev = None
        self.twin = None
        self.next = None
        self.face = None

class Face:
    def __init__(self, index, outer_component=None, inner_component=None, site=None):
        self.index = index
        self.outer_component = outer_component
        self.inner_component = inner_component
        self.site = site

class DCEL:
    def __init__(self):
        self.vertices_list = []
        self.half_edges_list = []
        self.faces_list = []
        self.sites_list = []

    def create_vertex(self, x, y, index):
        point = Point(x, y)
        vertex = Vertex(point, index)
        self.vertices_list.append(vertex)
        return vertex
    
    def create_half_edge(self, origin, destination):
        # create 2 half edges
        edge = Half_Edge(origin, destination)
        twin_edge = Half_Edge(destination, origin)
        
        edge.face = self.create_face(1) # TODO DELETE ME
        twin_edge.face = self.create_face(1) # TODO DELETE ME

        # TODO FIX  next is not the next point, it is the next half edge for that cell
        edge.next = edge
        edge.prev = edge

        # TODO FIX  next is not the next point, it is the next half edge for that cell
        twin_edge.next = edge
        twin_edge.prev = edge

        # set twins
        edge.twin = twin_edge
        twin_edge.twin = edge

        # add to incident edge list
        origin.incident_edges_list.append(edge)
        destination.incident_edges_list.append(twin_edge)

        # append to DCEL lists
        self.half_edges_list.append(edge)
        self.half_edges_list.append(twin_edge)

        return edge
    
    def create_face(self, index):
        face = Face(index)
        self.faces_list.append(face)
        return face
    
    def create_site(self, x, y, index):
        point = Point(x, y)
        site = Site(point, index)
        self.sites_list.append(site)
        return site
    
    def write_vertices(self, file):
        for v in self.vertices_list:
            print("v{} ({}, {})".format(v.index, v.point.x, v.point.y), end='')
            
            for e in v.incident_edges_list:
                print(" e{},{}".format(e.origin.index, e.next.index), end='')
        
            print()


    
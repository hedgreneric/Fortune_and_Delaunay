import math as m
from point import Point

class Site:
    def __init__(self):
        self.index
        self.point
        self.face

class Vertex:
    def __init__(self, point, index):
        self.index = index
        self.point = point
        self.incident_edges_list = [] # Incident Edges

class Half_Edge:
    def __init__(self):
        self.origin = None
        self.prev = None
        self.twin = None
        self.next = None
        self.face = None
        

class Face:
    def __init__(self, index):
        self.index = index
        self.outer_component = None
        self.inner_component = None

class DCEL:
    def __init__(self):
        self.vertices_list = []
        self.half_edges_list = []
        self.faces_list = []

    def add_vertex(self, x, y, index):
        point = Point(x, y)
        vertex = Vertex(point, index)
        self.vertices_list.append(vertex)
        return vertex
    
    def add_edge(self, origin, destination):
        edge = Half_Edge()
        edge.origin = origin
        edge.next = destination
        origin.incident_edges_list.append(edge)
        twin_edge = Half_Edge()
        twin_edge.origin = destination
        # destination.incident_edges_list.append(twin_edge)
        edge.twin = twin_edge
        twin_edge.twin = edge
        self.half_edges_list.append(edge)
        self.half_edges_list.append(twin_edge)
        return edge
    
    def add_face(self, index):
        face = Face(index)
        self.faces_list.append(face)
        return face
    
    def print_vertices(self):
        for v in self.vertices_list:
            print("v{} ({}, {})".format(v.index, v.point.x, v.point.y), end='')
            
            for e in v.incident_edges_list:
                print(" e{},{}".format(e.origin.index, e.next.index), end='')
        
            print()

    
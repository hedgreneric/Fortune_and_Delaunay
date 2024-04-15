import math as m

class Site:
    def __init__(self):
        self.index

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.incident_edges_list = [] # Incident Edges

class Half_Edge:
    def __init__(self, v1, v2):
        self.origin = None
        self.prev = None
        self.twin = None
        self.next = None
        self.face = None
        

class Face:
    def __init__(self):
        self.outer_component = None
        self.inner_component = None

class DCEL:
    def __init__(self):
        self.vertices_list = []
        self.half_edges_list = []
        self.faces_list = []

    def add_vertex(self, x, y):
        vertex = Vertex(x, y)
        self.vertices_list.append(vertex)
        return vertex
    
    def add_edge(self, origin, destination):
        edge = Half_Edge()
        edge.origin = origin
        twin_edge = Half_Edge()
        twin_edge.origin = destination
        edge.twin = twin_edge
        twin_edge.twin = edge
        self.half_edges_list.append(edge)
        self.half_edges_list.append(twin_edge)
        return edge
    
    def add_face(self):
        face = Face()
        self.faces_list.append(face)
        return face
    
    def print_vertices(self):
        for i in range(0, len(self.vertices_list)):
            print("v{} ({}, {})".format((i + 1), self.vertices_list[i].x, self.vertices_list[i].y, ))

    
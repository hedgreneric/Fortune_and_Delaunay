import math as m
from point import Point

class Vertex:
    def __init__(self, point=None, index=None):
        self.index:int = index or -1
        self.point:Point = point or Point()
        self.incident_edges_list:list[Half_Edge] = [] # Incident Edges

class Half_Edge:
    def __init__(self):
        self.origin:Vertex = Vertex()
        self.destination:Vertex = Vertex()
        self.prev:Half_Edge = None
        self.twin:Half_Edge = None
        self.next:Half_Edge = None
        self.face:Face = Face()

class Face:
    def __init__(self, index=-1, outer_component=None, inner_component=None, site=None):
        self.index:int = index
        self.outer_component:Half_Edge = outer_component
        self.inner_component:Half_Edge = inner_component
        self.site:Site = site

class Site:
    def __init__(self, point=None, index=None, face=None):
        self.index:int = index or -1
        self.point:Point = point or Point()
        self.face:Face = face

class DCEL:
    def __init__(self):
        self.vertices_list:list[Vertex] = []
        self.half_edges_list:list[Half_Edge] = []
        self.faces_list:list[Face] = []
        self.sites_list:list[Site] = []

    def create_vertex(self, point:Point, index:int=-1):
        if index == -1: index = len(self.vertices_list)
        vertex = Vertex(point, index)

        self.vertices_list.append(vertex)
        return vertex
    
    def create_half_edge(self, face:Face):
        half_edge = Half_Edge()
        half_edge.face = face

        self.half_edges_list.append(half_edge)

        if face.outer_component is None:
            face.outer_component = half_edge

        return half_edge
    
    def create_face(self, index):
        face = Face(index)
        self.faces_list.append(face)
        return face
    
    def create_site(self, x, y, index):
        point = Point(x, y)
        face = self.create_face(index)
        site = Site(point, index, face)
        site.face.site = site
        self.sites_list.append(site)
        return site
    
    def write_vertices(self, file):
        for v in self.vertices_list:
            print("v{} ({}, {})".format(v.index, v.point.x, v.point.y), end='')
            
            for e in v.incident_edges_list:
                print(" e{},{}".format(e.origin.index, e.next.index), end='')
        
            print()


    
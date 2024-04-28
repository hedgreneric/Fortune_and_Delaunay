import math as m
from point import Point

class Site:
    def __init__(self, point, index):
        self.index:int = index
        self.point:Point = point
        self.face:Face = None

class Vertex:
    def __init__(self, point, index):
        self.index:int = index
        self.point:Point = point
        self.incident_edges_list:list[Half_Edge] = [] # Incident Edges

class Half_Edge:
    def __init__(self, origin=None, destination=None):
        self.origin:Vertex = origin
        self.destination:Vertex = destination
        self.prev:Half_Edge = None
        self.twin:Half_Edge = None
        self.next:Half_Edge = None
        self.face:Face = None

class Face:
    def __init__(self, index, outer_component=None, inner_component=None, site=None):
        self.index:int = index
        self.outer_component:Half_Edge = outer_component
        self.inner_component:Half_Edge = inner_component
        self.site:Site = site

class DCEL:
    def __init__(self):
        self.vertices_list:list[Vertex] = []
        self.half_edges_list:list[Half_Edge] = []
        self.faces_list:list[Face] = []
        self.sites_list:list[Site] = []

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


    
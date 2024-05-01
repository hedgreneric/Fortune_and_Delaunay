import math as m
from point import Point
from box import Box
from box import Side
from box import Intersection

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
        self.index:int = index or 0
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
            face.outer_component = self.half_edges_list[-1]

        return self.half_edges_list[-1]
    
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
    
    def get_face(self, i:int):
        return self.faces_list[i]
    
    def box_intersect(self, box:Box):
        is_error:bool = False
        processed_half_edges_list:list[Half_Edge] = []
        remove_vertices_list:list[Vertex] = []

        for site in self.sites_list:
            he:Half_Edge = site.face.outer_component
            is_in:bool = box.contains(he.origin.point)
            out_messed_up:bool = not is_in

            in_he:Half_Edge = None
            out_he:Half_Edge = None

            in_side:Side
            out_side:Side

            while True:
                intersections_list = [Intersection(), Intersection()]

                num_intersections:int = box.get_intersections(he.origin.point, he.destination.point, intersections_list)
                is_next_in:bool = box.contains(he.destination.point)
                next_he:Half_Edge = he.next

                if not is_in and not is_next_in:
                    if num_intersections == 0:
                        remove_vertices_list.append(he.origin)
                        self.remove_half_edge(he)
                    elif num_intersections == 2:
                        remove_vertices_list.append(he.origin)
                        if he.twin in processed_half_edges_list:
                            he.origin = he.twin.destination
                            he.destination = he.twin.origin
                        else:
                            he.origin = self.create_vertex(intersections_list[0].point)
                            he.destination = self.create_vertex(intersections_list[1].point)
                        
                        if out_he is not None:
                            self.link(box, out_he, out_side, he, intersections_list[0].side)
                        
                        if in_he is None:
                            in_he = he
                            in_side = intersections_list[0].side
                        
                        out_he = he
                        in_side = intersections_list[1].side
                        processed_half_edges_list.append(he)
                    else:
                        is_error = True

                elif is_in and not is_next_in:
                    if num_intersections == 1:
                        if he.twin in processed_half_edges_list:
                            he.destination = he.twin.origin
                        else:
                            he.destination = he.twin.origin
                    else:
                        is_error = True
                elif not is_in and is_next_in:
                    if num_intersections == 1:
                        remove_vertices_list.append(he.origin)
                        if he.twin in processed_half_edges_list:
                            he.origin = he.twin.destination
                        else:
                            he.origin = self.create_vertex(intersections_list[0].point)
                        
                        if out_he is None:
                            self.link(box, out_he, out_side, he, intersections_list[0].side)

                        if in_he is None:
                            in_he = he
                            in_side = intersections_list[0].side
                        
                        processed_half_edges_list.append(he)
                    else:
                        is_error = True
                    
                    he = next_he

                    is_in = is_next_in

                if he is not site.face.outer_component:
                    break

            if out_messed_up and in_he is not None:
                self.link(box, out_he, out_side, in_he, in_side)   
            if out_messed_up:
                site.face.outer_component= in_he

        for v in remove_vertices_list:
            self.remove_vertex(v)

        return not is_error  
    
    def link(self, box:Box, start:Half_Edge, start_side:Side, end:Half_Edge, end_side:Side):
        he:Half_Edge = start
        side:Side = start_side

        while not (side == end_side.value):
            side = Side((side.value + 1) % 4)
            he.next = self.create_half_edge(start.face)
            he.next.prev = he
            he.next.origin = he.destination
            he.next.destination = self.create_corner(box, side)
            he = he.next
        
        he.next = self.create_half_edge(start.face)
        he.next.prev = he
        end.prev = he.next
        he.next.next = end
        he.next.origin = he.destination
        he.next.destination = end.origin

    def create_corner(self, box:Box, side:Side):
        if side == Side.LEFT:
            return self.create_vertex(Point(box.left, box.top))
        elif side == Side.BOTTOM:
            return self.create_vertex(Point(box.left, box.bottom))
        elif side == Side.RIGHT:
            return self.create_vertex(Point(box.right, box.bottom))
        else:
            return self.create_vertex(Point(box.right, box.top))
    
    def remove_vertex(self, v:Vertex):
        self.vertices_list.remove(v)
    
    def remove_half_edge(self, he):
        self.half_edges_list.remove(he)
            

    
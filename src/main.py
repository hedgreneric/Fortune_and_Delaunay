import dcel as DCEL
from point import Point
import fortune
from box import Box

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

voronoi_dcel = DCEL.DCEL()
delaunay_dcel = DCEL.DCEL()

def point_convert_in(x, y):
    return (x + 23), (y + 14)

def point_converter_out(x, y):
    """ Convert the points given in the txt to valid points on the screen.
        Also have (0,0) be in the center
    """

    x_shift = 512
    y_shift = (x_shift * .75)

    point_range_x = 24
    point_range_y = point_range_x * .75
    point_multiplier = (x_shift / point_range_x) # 512 / 20 or 384 / 15

    return (((x - point_range_x - 1) * point_multiplier) + x_shift), (((y - point_range_y - 1) * point_multiplier) + y_shift)


def draw_line(p1:Point, p2:Point, color):
    """ Draw a line using OpenGL
    """
    if color == "R":
        glColor3f(1.0, 0.0, 0.0)
    elif color == "B":
        glColor3f(0.0, 0.0, 1.0)
    elif color == "G":
        glColor3f(0.0, 1.0, 0.0)
    elif color == "W":
        glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_LINES)
    x, y = point_converter_out(p1.x, p1.y)
    glVertex2f(x, y)

    x, y = point_converter_out(p2.x, p2.y)
    glVertex2f(x, y)
    glEnd()

def draw_edges(dcel:DCEL.DCEL):
    for site in dcel.sites_list:
        center = site.point
        face = site.face
        half_edge = face.outer_component
        if half_edge is None:
            continue
        while half_edge.prev is not None:
            half_edge = half_edge.prev
            if half_edge is face.outer_component:
                break
        start = half_edge
        while half_edge is not None:
            if half_edge.origin is not None and half_edge.destination is not None:
                origin = half_edge.origin.point
                destination = half_edge.destination.point
                draw_line(origin, destination, "R")
            half_edge = half_edge.next
            if half_edge is start:
                break

        


def draw_point(v, color, size=5):
    """Draw a point using OpenGL
    """
    if color == "R":
        glColor3f(1.0, 0.0, 0.0)
    elif color == "B":
        glColor3f(0.0, 0.0, 1.0)
    elif color == "G":
        glColor3f(0.0, 1.0, 0.0)

    glPointSize(size)
    glBegin(GL_POINTS)

    x, y = point_converter_out(v.point.x, v.point.y)

    glVertex2f(x, y)
    glEnd()

def write_vertices(f, dcel):
    for v in dcel.vertices_list:
        f.write("v{} ({}, {})".format(v.index + 1, v.point.x, v.point.y))
        
        for e in v.incident_edges_list:
            f.write(" e{},{}".format(e.origin.index + 1, e.destination.index + 1))
    
        f.write("\n")
    f.write("\n")

def write_faces(f, dcel):
    for face in dcel.faces_list:
        f.write("v{}".format(face.index + 1))
        
        if face.outer_component == None:
            f.write(" nil")
        else:
            f.write(" e{},{}".format(face.outer_component.origin.index + 1,
                                        face.outer_component.destination.index + 1))

        if face.inner_component == None:
            f.write(" nil")
        else:
            f.write(" e{},{}".format(face.inner_component.origin.index + 1,
                                        face.inner_component.destination.index + 1))
    
        f.write("\n")
    f.write("\n")

def write_half_edges(f, dcel):
    for e in dcel.half_edges_list:
        f.write("e{},{}".format(e.origin.index + 1, e.destination.index + 1))
        f.write(" v{}".format(e.origin.index + 1))
        f.write(" e{},{}".format(e.twin.origin.index + 1, e.twin.destination.index + 1))
        f.write(" f{}".format(e.face.index + 1))
        f.write(" e{},{}".format(e.next.origin.index + 1, e.next.destination.index + 1))
        f.write(" e{},{}".format(e.prev.origin.index + 1, e.prev.destination.index + 1))

        f.write("\n")

if __name__ == '__main__':
    
    in_file_path = input("Enter input file path: ")
    
    site_index = 0

    if in_file_path == '':
        for i in range(random.randint(3, 20)):
            x = random.randint(-23, 23)
            y = random.randint(-14, 14)

            # x, y = point_convert_in(x, y)
            voronoi_dcel.create_site(x, y, site_index)
            delaunay_dcel.create_vertex(Point(x, y), site_index)

            site_index += 1

    else:
        with open(in_file_path, 'r') as sites_file:
            for line in sites_file:
                line = line.replace('(', '').replace(')', '').replace(',', '').split()
                
                for i in range(0, len(line), 2):
                    x, y = map(int, line[i:i+2])

                    x, y = point_convert_in(x, y)
                    voronoi_dcel.create_site(x, y, site_index)
                    # delaunay_dcel.create_vertex(x, y, site_index)

                    site_index += 1

    voronoi_diagram = fortune.Voronoi_Diagram(voronoi_dcel)
    voronoi_diagram.fortune_algorithm()
    voronoi_diagram.bound_box(Box(-0.05, -0.05, 1.05, 1.05))
    
    # TODO function call to generate Delaunay Triangulation

    # TODO ensure that next and prev of all edges are filled in or it will error
    
    # write dcels to file
    with open("voronoi.txt", 'w') as f:
        f.write("****** Voronoi diagram ******\n\n")
        write_vertices(f, voronoi_dcel)
        write_faces(f, voronoi_dcel)
        # write_half_edges(f, voronoi_dcel)

        f.write("\n\n****** Delaunay triangulation ******\n\n")        
        write_vertices(f, delaunay_dcel)
        write_faces(f, delaunay_dcel)
        write_half_edges(f, delaunay_dcel)


    pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Voronoi Diagram and Delaunay Triangulation")

    # Set up 2D orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 1024, 0, 768, -1, 1)  # (left, right, bottom, top, near, far)

    # Set up model-view matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw red lines and points
        # for e in voronoi_dcel.half_edges_list:
        #     draw_line(e.origin, e.destination, "R")
        draw_edges(voronoi_dcel)

        # for v in voronoi_dcel.vertices_list:
        #     draw_point(v, "R")

        for s in voronoi_dcel.sites_list:
            draw_point(s, "G")

        # for e in delaunay_dcel.half_edges_list:
        #     draw_line(e.origin, e.destination, "B")
            
        # Swap buffers to show the drawn objects
        pygame.display.flip()

    pygame.quit()
    


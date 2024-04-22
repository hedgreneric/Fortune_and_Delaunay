import dcel as dcel
from point import Point

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def point_converter(x, y):
    """ Convert the points given in the txt to valid points on the screen.
        Also have (0,0) be in the center
    """
    point_range = 25 # 512 / 20 or 384 / 15
    x_shift = 512
    y_shift = 384
    return ((x * point_range) + x_shift), ((y * point_range) + y_shift)


def draw_line(v1, v2, color):
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
    x, y = point_converter(v1.point.x, v1.point.y)
    glVertex2f(x, y)

    x, y = point_converter(v2.point.x, v2.point.y)
    glVertex2f(x, y)
    glEnd()


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

    x, y = point_converter(v.point.x, v.point.y)

    glVertex2f(x, y)
    glEnd()

def write_vertices(f, dcel):
    for v in dcel.vertices_list:
        f.write("v{} ({}, {})".format(v.index, v.point.x, v.point.y))
        
        for e in v.incident_edges_list:
            f.write(" e{},{}".format(e.origin.index, e.destination.index))
    
        f.write("\n")
    f.write("\n")

def write_faces(f, dcel):
    for face in dcel.faces_list:
        f.write("v{}".format(face.index))
        
        if face.outer_component == None:
            f.write(" nil")
        else:
            f.write(" e{},{}".format(face.outer_component.origin.index,
                                        face.outer_component.destination.index))

        if face.inner_component == None:
            f.write(" nil")
        else:
            f.write(" e{},{}".format(face.inner_component.origin.index,
                                        face.inner_component.destination.index))
    
        f.write("\n")
    f.write("\n")

def write_half_edges(f, dcel):
    for e in dcel.half_edges_list:
        f.write("e{},{}".format(e.origin.index, e.destination.index))
        f.write(" v{}".format(e.origin.index))
        f.write(" e{},{}".format(e.twin.origin.index, e.twin.destination.index))
        f.write(" f{}".format(e.face.index))
        f.write(" e{},{}".format(e.next.origin.index, e.next.destination.index))
        f.write(" e{},{}".format(e.prev.origin.index, e.prev.destination.index))

        f.write("\n")

if __name__ == '__main__':
    
    in_file_path = input("Enter input file path: ")
    
    site_index = 1

    voronoi_dcel = dcel.DCEL()
    delaunay_dcel = dcel.DCEL()

    with open(in_file_path, 'r') as sites_file:
        for line in sites_file:
            line = line.replace('(', '').replace(')', '').replace(',', '').split()
            
            for i in range(0, len(line), 2):
                x, y = map(int, line[i:i+2])
                voronoi_dcel.create_site(x, y, site_index)
                delaunay_dcel.create_vertex(x, y, site_index)

                voronoi_dcel.create_vertex(x, y, site_index) # DELETE ME
                site_index += 1

    # todo calls to functions to generate voronoi diagram
    # and delaunay triangulation

    # DELETE ME
    voronoi_dcel.create_half_edge(voronoi_dcel.vertices_list[0],
                                    voronoi_dcel.vertices_list[1])
    voronoi_dcel.create_half_edge(voronoi_dcel.vertices_list[1],
                                    voronoi_dcel.vertices_list[2])
    voronoi_dcel.create_half_edge(voronoi_dcel.vertices_list[2],
                                    voronoi_dcel.vertices_list[3])
    voronoi_dcel.create_half_edge(voronoi_dcel.vertices_list[3],
                                    voronoi_dcel.vertices_list[0])
    
    # write dcels to file
    with open("voronoi.txt", 'w') as f:
        f.write("****** Voronoi diagram ******\n\n")
        write_vertices(f, voronoi_dcel)
        write_faces(f, voronoi_dcel)
        write_half_edges(f, voronoi_dcel)

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

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw red lines and points
        for e in voronoi_dcel.half_edges_list:
            draw_line(e.origin, e.destination, "R")

        for v in voronoi_dcel.vertices_list:
            draw_point(v, "R")

        for s in voronoi_dcel.sites_list:
            draw_point(s, "G")

        for e in delaunay_dcel.half_edges_list:
            draw_line(e.origin, e.destination, "B")
            
        # Swap buffers to show the drawn objects
        pygame.display.flip()

    pygame.quit()
    


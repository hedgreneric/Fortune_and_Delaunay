import dcel as dcel
from point import Point

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def point_converter(x, y):
    return ((x * 25) + 512), ((y * 25) + 384)

def draw_line(v1, v2, color):

    if color == "R":
        glColor3f(1.0, 0.0, 0.0)
    elif color == "B":
        glColor3f(0.0, 0.0, 1.0)

    glBegin(GL_LINES)
    x, y = point_converter(v1.point.x, v1.point.y)
    glVertex2f(x, y)

    x, y = point_converter(v2.point.x, v2.point.y)
    glVertex2f(x, y)
    glEnd()

def draw_point(v, color, size=5):
    if color == "R":
        glColor3f(1.0, 0.0, 0.0)
    elif color == "B":
        glColor3f(0.0, 0.0, 1.0)

    glPointSize(size)
    glBegin(GL_POINTS)

    x, y = point_converter(v.point.x, v.point.y)

    glVertex2f(x, y)
    glEnd()

if __name__ == '__main__':
    
    in_file_path = input("Enter input file path: ")
    
    num_sites = 1

    dcel = dcel.DCEL()

    with open(in_file_path, 'r') as sites_file:
        for line in sites_file:
            line = line.replace('(', '').replace(')', '').replace(',', '').split()
            
            for i in range(0, len(line), 2):
                x, y = map(int, line[i:i+2])
                dcel.create_vertex(x, y, num_sites)
                num_sites += 1

        dcel.create_half_edge(dcel.vertices_list[0], dcel.vertices_list[1])
        dcel.create_half_edge(dcel.vertices_list[1], dcel.vertices_list[2])
        dcel.create_half_edge(dcel.vertices_list[2], dcel.vertices_list[3])
        dcel.create_half_edge(dcel.vertices_list[3], dcel.vertices_list[0])
        dcel.create_half_edge(dcel.vertices_list[0], dcel.vertices_list[2])


    pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

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
        for e in dcel.half_edges_list:
            draw_line(e.origin, e.destination, "R")

        for v in dcel.vertices_list:
            draw_point(v, "R")
            
        # Swap buffers to show the drawn objects
        pygame.display.flip()

    pygame.quit()

    
        


    # dcel.print_vertices()
    


from OpenGL.GL import *
from OpenGL.GLUT import *

from geometry import *
from camera import *

camera = Camera('camera.txt')
geometry = Geometry('geometry.d.txt')
geometry.world_to_screen(camera)


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5.0)
    for polygon in geometry.polygon_list:
        # filter back face (if need)
        if polygon[2]:
            # draw line
            glBegin(GL_LINE_LOOP)
            for index in polygon[0]:
                # draw point
                glVertex2f(geometry.screen_point_list[index][0], geometry.screen_point_list[index][1])
            glEnd()
    glFlush()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(600, 600)
    glutCreateWindow("Geometry")
    glutDisplayFunc(draw)
    glutMainLoop()
    return


if __name__ == '__main__':
    main()

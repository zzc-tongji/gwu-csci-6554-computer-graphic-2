from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import datetime
import math


class Texture(object):

    def __init__(self, enable=False):
        self.__pixel_number = 800
        self.__divider = self.__pixel_number / 16
        self.__color_1 = [1, 0, 0]
        self.__color_2 = [0, 0, 1]
        self.__i_buffer = [None] * self.__pixel_number
        for i in range(0, len(self.__i_buffer)):
            if 1 <= i / self.__divider <= 3 or 5 <= i / self.__divider <= 7 \
                    or 9 <= i / self.__divider <= 11 or 13 <= i / self.__divider <= 15:
                self.__i_buffer[i] = [self.__color_2] * self.__pixel_number
            else:
                self.__i_buffer[i] = [self.__color_1] * self.__pixel_number
        self.enable = enable

    def __draw(self):
        print('Rendering ...')
        start = datetime.datetime.now()
        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_POINTS)
        for i in range(0, len(self.__i_buffer)):
            for j in range(0, len(self.__i_buffer[i])):
                glColor3fv(self.__i_buffer[i][j])
                glVertex2i(j, i)
        glEnd()
        glFlush()
        render_cost = datetime.datetime.now() - start
        print('Finish. (cost = ' + str(render_cost) + ')\n')

    def show(self):
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
        glutInitWindowSize(self.__pixel_number, self.__pixel_number)
        glutCreateWindow('')
        gluOrtho2D(0, self.__pixel_number, 0, self.__pixel_number)
        glutDisplayFunc(self.__draw)
        glutMainLoop()

    def calculate(self, mr4c1):
        point = mr4c1
        x = float(point[0][0])
        y = float(point[1][0])
        z = float(point[2][0])
        if x > 1:
            x = 1
        elif x < -1:
            x = -1
        if y > 1:
            y = 1
        elif y < -1:
            y = -1
        try:
            if z >= 0:
                z = math.sqrt(1 - x ** 2 - y ** 2)
            else:
                z = -math.sqrt(1 - x ** 2 - y ** 2)
        except ValueError:
            return self.__color_1
        theta = math.acos(z)
        v = 16 * (theta / math.pi)
        if 1 <= v <= 3 or 5 <= v <= 7 or 9 <= v <= 11 or 13 <= v <= 15:
            return self.__color_2
        return self.__color_1


if __name__ == '__main__':
    texture = Texture()
    texture.show()

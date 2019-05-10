import datetime
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from display import Display
from space import Space
from aet import AET


class Window(object):

    def __init__(self):
        # input
        self.__device_space = None
        self.__display = None
        # calculate
        self.__polygon_list_back_face = None
        self.__polygon_list_color = None
        self.__polygon_list_aet = None
        self.__z_buffer = None  # coordinate z of the pixel
        self.__w_buffer = None  # coordinate w of the pixel
        self.__i_buffer = None  # the color (RGB) of the pixel
        self.__p_buffer = None  # the polygon which the pixel belongs to
        # ready
        self.__is_ready = False

    def set(self, device_space, display):
        if not isinstance(device_space, Space):
            raise Exception('There is a type error in parameter `device_space`.')
        if not isinstance(display, Display) or not display.is_ready:
            raise Exception('Display is not ready.')
        self.__device_space = device_space
        self.__display = display
        self.__calculate()

    def __calculate(self):
        # polygon
        len_polygon = len(self.__device_space.polygon_list_vertex_list)
        self.__polygon_list_back_face = [False] * len_polygon
        self.__polygon_list_color = [None] * len_polygon
        self.__polygon_list_aet = [None] * len_polygon
        for i in range(1, len_polygon):
            # back-face culling
            if self.__device_space.polygon_list_normal_vector[i][2][0] >= 0:
                self.__polygon_list_back_face[i] = True
            # generate color (RGB) for each polygon randomly
            self.__polygon_list_color[i] = \
                [random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)]
            # generate active edge table (AET)
            if self.__polygon_list_back_face[i]:
                # ignore back-face polygon
                continue
            self.__polygon_list_aet[i] = AET()
            self.__polygon_list_aet[i].set(
                self.__device_space.vertex_list_coordinate,
                self.__device_space.polygon_list_vertex_list[i],
                self.__device_space.polygon_list_edge_list_vertex_index[i]
            )
        # pixel
        self.__z_buffer = []
        self.__w_buffer = []
        self.__i_buffer = []
        self.__p_buffer = []
        for i in range(0, self.__display.pixel_number + 1):
            self.__z_buffer.append([])
            self.__w_buffer.append([])
            self.__i_buffer.append([])
            self.__p_buffer.append([])
            for j in range(0, self.__display.pixel_number + 1):
                self.__z_buffer[-1].append(float('Inf'))
                self.__w_buffer[-1].append(float('Inf'))
                self.__i_buffer[-1].append([0, 0, 0])
                self.__p_buffer[-1].append(0)
        # iterate each polygon
        for i in range(1, len(self.__polygon_list_aet)):
            if self.__polygon_list_back_face[i]:
                # ignore back-face polygon
                continue
            # iterate each scan line
            for j in range(0, len(self.__polygon_list_aet[i].active_edge_table)):
                if self.__polygon_list_aet[i].active_edge_table[j] is not None:
                    scan_line = self.__polygon_list_aet[i].active_edge_table[j]
                    len_scan_line = len(scan_line)
                    if len_scan_line % 2 != 0:
                        # ignore the wrong situation (each scan line should contain even edges)
                        len_scan_line -= 1
                    for k in range(0, len_scan_line, 2):
                        x_a = scan_line[k].bottom_vertex_x
                        x_b = scan_line[k + 1].bottom_vertex_x
                        for l in range(round(x_a), round(x_b)):
                            x = l
                            y = j + self.__polygon_list_aet[i].offset_y
                            if 0 <= x <= self.__display.pixel_number and 0 <= y <= self.__display.pixel_number:
                                v0 = self.__device_space.vertex_list_coordinate[
                                    self.__device_space.polygon_list_vertex_list[i][0]
                                ]
                                v1 = self.__device_space.vertex_list_coordinate[
                                    self.__device_space.polygon_list_vertex_list[i][1]
                                ]
                                v2 = self.__device_space.vertex_list_coordinate[
                                    self.__device_space.polygon_list_vertex_list[i][2]
                                ]
                                # avoid "divide 0" error
                                if (v0[1][0] - v1[1][0] == 0 and v0[1][0] - v2[1][0] == 0) \
                                        or (v0[1][0] - v2[1][0] == 0 and v1[1][0] - v2[1][0] == 0) \
                                        or (v0[1][0] - v1[1][0] == 0 and v1[1][0] - v2[1][0] == 0):
                                    raise Exception(
                                        'Coordinates y are same '
                                        '(location: polygon #' + str(i) + ', AET scan line #' + str(j) + ').'
                                    )
                                if v0[1][0] - v1[1][0] == 0:
                                    temp = v0
                                    v0 = v2
                                    v2 = temp
                                if v0[1][0] - v2[1][0] == 0:
                                    temp = v0
                                    v0 = v1
                                    v1 = temp
                                # interpolate z
                                z_a = v0[2][0] - (v0[2][0] - v1[2][0]) * (v0[1][0] - y) / (v0[1][0] - v1[1][0])
                                z_b = v0[2][0] - (v0[2][0] - v2[2][0]) * (v0[1][0] - y) / (v0[1][0] - v2[1][0])
                                z = z_b - (z_b - z_a) * (x_b - x) / (x_b - x_a)
                                if z < self.__z_buffer[x][y]:
                                    self.__z_buffer[x][y] = z
                                    # interpolate w
                                    w_a = v0[3][0] - (v0[3][0] - v1[3][0]) * (v0[1][0] - y) / (v0[1][0] - v1[1][0])
                                    w_b = v0[3][0] - (v0[3][0] - v2[3][0]) * (v0[1][0] - y) / (v0[1][0] - v2[1][0])
                                    w = w_b - (w_b - w_a) * (x_b - x) / (x_b - x_a)
                                    self.__w_buffer[x][y] = w
                                    self.__i_buffer[x][y] = self.__polygon_list_color[i]
                                    self.__p_buffer[x][y] = i
        # ready
        self.is_ready = True

    def __draw(self):
        test = False
        print('Rendering ...')
        start = datetime.datetime.now()
        glClear(GL_COLOR_BUFFER_BIT)
        if test:
            # test: framework without back-face
            glPointSize(1)
            for i in range(1, len(self.__device_space.polygon_list_vertex_list)):
                if not self.__polygon_list_back_face[i]:
                    # draw line
                    glBegin(GL_LINE_LOOP)
                    for vertex_index in self.__device_space.polygon_list_vertex_list[i]:
                        # draw point
                        glVertex2f(
                            self.__device_space.vertex_list_coordinate[vertex_index][0][0],
                            self.__device_space.vertex_list_coordinate[vertex_index][1][0]
                        )
                    glEnd()
        else:
            glBegin(GL_POINTS)
            for i in range(0, self.__display.pixel_number + 1):
                for j in range(0, self.__display.pixel_number + 1):
                    if self.__p_buffer[i][j] == 0:
                        # accelerate: ignore "non-polygon" pixels
                        continue
                    glColor3ubv(self.__i_buffer[i][j])
                    glVertex2i(i, j)
            glEnd()
        glFlush()
        render_cost = datetime.datetime.now() - start
        print('Finish. (cost = ' + str(render_cost) + ')\n')

    def show(self):
        if not self.is_ready:
            raise Exception('Window is not ready.')
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
        glutInitWindowSize(self.__display.pixel_number, self.__display.pixel_number)
        glutCreateWindow("")
        gluOrtho2D(0, self.__display.pixel_number, 0, self.__display.pixel_number)
        glutDisplayFunc(self.__draw)
        glutMainLoop()

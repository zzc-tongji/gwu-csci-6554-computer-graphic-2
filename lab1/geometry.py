import os
import numpy as np

from camera import *


class Geometry(object):

    def __init__(self, file_path):
        self.screen_point_list = []
        self.world_point_list = []
        self.polygon_list = []
        # get point number and polygon number
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + file_path) as file:
            line_list = file.readlines()
        line = line_list[0].split()
        point_number = int(line[1])
        polygon_number = int(line[2])
        # generate world point list
        for i in range(1, 1 + point_number):
            line = line_list[i].split()
            # world point
            self.world_point_list.append(np.array([float(line[0]), float(line[1]), float(line[2])]))
        # generate polygon list
        for i in range(1 + point_number, 1 + point_number + polygon_number):
            line = line_list[i].split()
            # point index list
            point_index_list = []
            for j in range(1, len(line)):
                point_index_list.append(int(line[j]) - 1)
            # normal vector
            #
            # Data description (of ".d" file) says:
            #
            # "polygons given by: number of points in the polygon followed by vertex number in clockwise order
            # (when looking from outside the object)"
            #
            # It means that:
            #
            # If using (p0->p1) x (p1->p2) to calculate the normal vector N of the polygon,
            # N will points to the INSIDE of the geometry.
            #
            # However, N should point to the OUTSIDE in this graphic system.
            # As a result, using (p1->p2) x (p0->p1) to calculate the normal vector N.
            p0p1 = self.world_point_list[point_index_list[1]] - self.world_point_list[point_index_list[0]]
            p1p2 = self.world_point_list[point_index_list[2]] - self.world_point_list[point_index_list[1]]
            normal_vector = np.cross(p1p2, p0p1)
            # render (display or not)
            render = True
            # polygon
            polygon = [point_index_list, normal_vector, render]
            self.polygon_list.append(polygon)

    def world_to_screen(self, camera):
        # 3D world coordinate ===> 3D screen coordinate
        for point in self.world_point_list:
            self.screen_point_list.append(camera.world_to_screen(point))
        # remove back face
        if camera.remove_back_face:
            for polygon in self.polygon_list:
                if np.dot(camera.n, polygon[1]) >= 0:
                    polygon[2] = False

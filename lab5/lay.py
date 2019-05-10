import numpy as np
import os


class Lay(object):
    def __init__(self):
        self.__m = self.m_world = None
        self.__r = self.m_world = None
        self.__s = self.m_world = None
        self.m_world = None
        self.m_world_inv = None
        self.is_ready = False

    def set(self, move=np.eye(4), rotate=np.eye(4), scale=np.eye(4)):
        if type(move) != np.ndarray or move.shape != (4, 4):
            raise Exception('Parameter `move` must be 4x4 numpy.ndarray')
        if type(rotate) != np.ndarray or rotate.shape != (4, 4):
            raise Exception('Parameter `rotate` must be 4x4 numpy.ndarray.')
        if type(scale) != np.ndarray or scale.shape != (4, 4):
            raise Exception('Parameter `scale` must or 4x4 numpy.ndarray')
        self.__m = move
        self.__r = rotate
        self.__s = scale
        self.__calculate()

    def set_by_file(self, file_path):
        # read file
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + file_path) as file:
            line_list = file.readlines()
        for line in line_list:
            line_split = line.split()
            if len(line_split) <= 0:
                continue
            elif line_split[0] == 'move':
                self.__m = np.array([
                    [float(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4])],
                    [float(line_split[5]), float(line_split[6]), float(line_split[7]), float(line_split[8])],
                    [float(line_split[9]), float(line_split[10]), float(line_split[11]), float(line_split[12])],
                    [float(line_split[13]), float(line_split[14]), float(line_split[15]), float(line_split[16])],
                ])
            elif line_split[0] == 'rotate':
                self.__r = np.array([
                    [float(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4])],
                    [float(line_split[5]), float(line_split[6]), float(line_split[7]), float(line_split[8])],
                    [float(line_split[9]), float(line_split[10]), float(line_split[11]), float(line_split[12])],
                    [float(line_split[13]), float(line_split[14]), float(line_split[15]), float(line_split[16])],
                ])
            elif line_split[0] == 'scale':
                self.__s = np.array([
                    [float(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4])],
                    [float(line_split[5]), float(line_split[6]), float(line_split[7]), float(line_split[8])],
                    [float(line_split[9]), float(line_split[10]), float(line_split[11]), float(line_split[12])],
                    [float(line_split[13]), float(line_split[14]), float(line_split[15]), float(line_split[16])],
                ])
        self.__calculate()

    def __calculate(self):
        self.m_world = np.dot(np.dot(self.__m, self.__r), self.__s)
        self.m_world_inv = np.linalg.inv(self.m_world)
        self.is_ready = True

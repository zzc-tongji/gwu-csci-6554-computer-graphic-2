import numpy as np


class Lay(object):
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.m_world = None
        self.m_world_inv = None
        self.is_ready = False

    def set(self, x, y, z):
        if type(x) != int and type(x) != float:
            raise Exception('Parameter `x` must be a number.')
        if type(y) != int and type(y) != float:
            raise Exception('Parameter `y` must be a number.')
        if type(z) != int and type(z) != float:
            raise Exception('Parameter `z` must be a number.')
        self.__x = x
        self.__y = y
        self.__z = z
        self.__calculate()

    def __calculate(self):
        self.m_world = np.eye()
        self.m_world[3][0] = self.__x
        self.m_world[3][1] = self.__y
        self.m_world[3][2] = self.__z
        self.m_world_inv = np.linalg.inv(self.m_world)
        self.is_ready = True

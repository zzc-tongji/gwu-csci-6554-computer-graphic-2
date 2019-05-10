import numpy as np
import os


class Camera(object):

    def __init__(self):
        # C
        self.__c = None
        # P_{ref}
        self.__p_ref = None
        # V'
        self.__v_prime = None
        # h
        self.__h = None
        # d
        self.__d = None
        # f
        self.__f = None
        # n, U, V
        self.n = None
        self.__u = None
        self.__v = None
        # R, T
        self.__r = None
        self.__t = None
        # M_{view}, # M_{pers}
        self.m_view = None
        self.m_pers = None
        # M_{view}^{-1}, # M_{pers}^{-1}
        self.m_view_inv = None
        self.m_pers_inv = None
        # ready
        self.is_ready = False

    def set(self, c, p_ref, v_prime, h, d, f):
        # set
        if type(c) != list or len(c) != 3 \
                or type(c[0]) != int or type(c[0]) != float \
                or type(c[1]) != int or type(c[1]) != float \
                or type(c[2]) != int or type(c[2]) != float:
            raise Exception('There is a type error in parameter `c`.')
        if type(p_ref) != list or len(p_ref) != 3 \
                or type(p_ref[0]) != int or type(p_ref[0]) != float \
                or type(p_ref[1]) != int or type(p_ref[1]) != float \
                or type(p_ref[2]) != int or type(p_ref[2]) != float:
            raise Exception('There is a type error in parameter `p_ref`.')
        if type(v_prime) != list or len(v_prime) != 3 \
                or type(v_prime[0]) != int or type(v_prime[0]) != float \
                or type(v_prime[1]) != int or type(v_prime[1]) != float \
                or type(v_prime[2]) != int or type(v_prime[2]) != float:
            raise Exception('There is a type error in parameter `v_prime`.')
        if type(h) != int and type(h) != float:
            raise Exception('Parameter `h` must be a number.')
        if type(d) != int and type(d) != float:
            raise Exception('Parameter `d` must be a number.')
        if type(f) != int and type(f) != float:
            raise Exception('Parameter `f` must be a number.')
        self.__c = np.array(c)
        self.__p_ref = np.array(p_ref)
        self.__v_prime = np.array(v_prime)
        self.__h = h
        self.__d = d
        self.__f = f
        self.__calculate()

    def set_by_file(self, file_path):
        # read file
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + file_path) as file:
            line_list = file.readlines()
        for line in line_list:
            line_split = line.split()
            if len(line_split) <= 0:
                continue
            if line_split[0] == 'C':
                self.__c = np.array([float(line_split[1]), float(line_split[2]), float(line_split[3])])
            elif line_split[0] == 'P_{ref}':
                self.__p_ref = np.array([float(line_split[1]), float(line_split[2]), float(line_split[3])])
            elif line_split[0] == 'V\'':
                self.__v_prime = np.array([float(line_split[1]), float(line_split[2]), float(line_split[3])])
            elif line_split[0] == 'h':
                self.__h = float(line_split[1])
            elif line_split[0] == 'd':
                self.__d = float(line_split[1])
            elif line_split[0] == 'f':
                self.__f = float(line_split[1])
        self.__calculate()

    def __calculate(self):
        # n, U, V
        temp = self.__p_ref - self.__c
        self.n = temp / np.linalg.norm(temp, 2)
        temp = np.cross(self.n, self.__v_prime)
        self.__u = temp / np.linalg.norm(temp, 2)
        self.__v = np.cross(self.__u, self.n)
        # R, T
        self.__r = np.eye(4)
        self.__r[0][:3] = self.__u
        self.__r[1][:3] = self.__v
        self.__r[2][:3] = self.n
        self.__t = np.eye(4)
        self.__t[0][3] = -self.__c[0]
        self.__t[1][3] = -self.__c[1]
        self.__t[2][3] = -self.__c[2]
        # M_{view}, # M_{pers}
        self.m_view = np.dot(self.__r, self.__t)
        self.m_pers = np.zeros((4, 4))
        self.m_pers[0][0] = self.__d / self.__h
        self.m_pers[1][1] = self.__d / self.__h
        self.m_pers[2][2] = self.__f / (self.__f - self.__d)
        self.m_pers[2][3] = -self.__d * self.m_pers[2][2]
        self.m_pers[3][2] = 1
        # M_{view}^{-1}, # M_{pers}^{-1}
        self.m_view_inv = np.linalg.inv(self.m_view)
        self.m_pers_inv = np.linalg.inv(self.m_pers)
        # ready
        self.is_ready = True

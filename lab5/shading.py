import os


class Shading(object):

    def __init__(self):
        self.shading_type = 0

    def set(self, shading_type):
        if type(shading_type) != int or shading_type < 0 or shading_type > 3:
            raise Exception('Parameter `shading_type` must be a integer in [0,3].')
        self.shading_type = shading_type

    def set_by_file(self, file_path):
        # read file
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + file_path) as file:
            line_list = file.readlines()
        for line in line_list:
            line_split = line.split()
            if len(line_split) <= 0:
                continue
            elif line_split[0] == "shading_type":
                temp = int(line_split[1])
                if temp < 0 or temp > 3:
                    raise Exception('Parameter `shading_type` must be a integer in [0,3].')
                self.shading_type = temp

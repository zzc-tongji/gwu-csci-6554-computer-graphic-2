import os


class Display(object):

    def __init__(self):
        self.pixel_number = 0
        self.is_ready = False

    def set(self, pixel_number):
        if type(pixel_number) != int or pixel_number <= 0 or pixel_number % 2 != 0:
            raise Exception('Parameter `pixel_number` must be a positive even integer.')
        self.pixel_number = pixel_number
        self.is_ready = True

    def set_by_file(self, file_path):
        # read file
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + file_path) as file:
            line_list = file.readlines()
        for line in line_list:
            line_split = line.split()
            if len(line_split) <= 0:
                continue
            elif line_split[0] == 'pixel_number':
                temp = int(line_split[1])
                if temp <= 0 or temp % 2 != 0:
                    raise Exception('Parameter `pixel_number` must be a positive even integer.')
                self.pixel_number = temp
        self.is_ready = True

class Display(object):

    def __init__(self):
        self.pixel_number = 0
        self.is_ready = False

    def set(self, pixel_number):
        if type(pixel_number) != int or pixel_number <= 0 or pixel_number % 2 != 0:
            raise Exception('Parameter `x_pixel_number` must be a positive even integer.')
        self.pixel_number = pixel_number
        self.__calculate()

    def __calculate(self):
        self.is_ready = True

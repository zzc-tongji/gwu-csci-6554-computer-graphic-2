import copy
import datetime

from camera import Camera
from display import Display
from illumination import Illumination
from light import Light
from material import Material
from space import Space
from transform import *
from window import Window


def main():
    print('Reading ...')
    start = datetime.datetime.now()

    # data source name
    data_source_name = 'better-ball.d'
    # shading type:
    #   0 - no shading (framework)
    #   1 - constant shading
    #   2 - Gouraud shading
    #   3 - Phong shading
    shading = 3

    world_space = Space()
    world_space.append_by_file(data_source_name + '.txt')  # geometry data

    camera = Camera()
    camera.set_by_file(data_source_name + '.camera.txt')  # camera profile

    light = Light()
    light.set_by_file(data_source_name + '.light.txt')  # light profile

    material = Material()
    material.set_by_file(data_source_name + '.material.txt')  # material profile

    illumination = Illumination()
    illumination.set(camera, light, material, shading)

    display = Display()
    display.set(800)  # change window size

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    print('Calculating: transform ...')
    start = datetime.datetime.now()

    view_space = copy.deepcopy(world_space)
    view_space.transform(world_to_view, camera)

    screen_space = copy.deepcopy(view_space)
    screen_space.transform(view_to_screen, camera)

    device_space = copy.deepcopy(screen_space)
    device_space.transform(screen_to_device, display)

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    window = Window()
    window.set(world_space, device_space, illumination, display)

    window.show()


if __name__ == '__main__':
    main()

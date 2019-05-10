import copy
import datetime
import os

from camera import Camera
from display import Display
from lay import Lay
from light import Light
from shading import Shading
from space import Space
from texture import Texture
from transform import *
from window import Window


def main():
    print('Reading ...')
    start = datetime.datetime.now()

    ball = 'data' + os.sep + 'better-ball.d'

    lay = Lay()
    lay.set_by_file(ball + '.lay.p')

    local_space = Space()
    local_space.append_by_file(ball)

    camera = Camera()
    camera.set_by_file('data' + os.sep + 'camera.p')

    display = Display()
    display.set_by_file('data' + os.sep + 'display.p')

    light = Light()
    light.set_by_file('data' + os.sep + 'light.p')

    shading = Shading()
    shading.set_by_file('data' + os.sep + 'shading.p')

    texture = Texture(True)  # enable texture (in Phong shading)

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    print('Calculating: transform ...')
    start = datetime.datetime.now()

    world_space = copy.deepcopy(local_space)
    world_space.transform(local_to_world, lay)

    device_space = copy.deepcopy(world_space)
    device_space.transform(world_to_view, camera)
    device_space.transform(view_to_screen, camera)
    device_space.transform(screen_to_device, display)

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    window = Window()
    window.set(world_space, device_space, camera, display, light, shading, texture, lay)
    window.show()


if __name__ == '__main__':
    main()

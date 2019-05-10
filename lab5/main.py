import copy
import datetime
import os

from camera import Camera
from display import Display
from lay import Lay
from light import Light
from shading import Shading
from space import Space
from transform import *
from window import Window


def main():
    print('Reading ...')
    start = datetime.datetime.now()

    ball_1 = 'data' + os.sep + 'better-ball.1.d'
    ball_2 = 'data' + os.sep + 'better-ball.2.d'
    ball_3 = 'data' + os.sep + 'better-ball.3.d'

    lay_ball_1 = Lay()
    lay_ball_1.set_by_file(ball_1 + '.lay.p')
    lay_ball_2 = Lay()
    lay_ball_2.set_by_file(ball_2 + '.lay.p')
    lay_ball_3 = Lay()
    lay_ball_3.set_by_file(ball_3 + '.lay.p')

    local_space_ball_1 = Space()
    local_space_ball_1.append_by_file(ball_1)
    local_space_ball_2 = Space()
    local_space_ball_2.append_by_file(ball_2)
    local_space_ball_3 = Space()
    local_space_ball_3.append_by_file(ball_3)

    camera = Camera()
    camera.set_by_file('data' + os.sep + 'camera.p')

    display = Display()
    display.set_by_file('data' + os.sep + 'display.p')

    light = Light()
    light.set_by_file('data' + os.sep + 'light.p')

    shading = Shading()
    shading.set_by_file('data' + os.sep + 'shading.p')

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    print('Calculating: transform ...')
    start = datetime.datetime.now()

    world_space = Space()

    temp = copy.deepcopy(local_space_ball_1)
    temp.transform(local_to_world, lay_ball_1)
    world_space.append_by_space(temp)

    temp = copy.deepcopy(local_space_ball_2)
    temp.transform(local_to_world, lay_ball_2)
    world_space.append_by_space(temp)

    temp = copy.deepcopy(local_space_ball_3)
    temp.transform(local_to_world, lay_ball_3)
    world_space.append_by_space(temp)

    device_space = copy.deepcopy(world_space)
    device_space.transform(world_to_view, camera)
    device_space.transform(view_to_screen, camera)
    device_space.transform(screen_to_device, display)

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    window = Window()
    window.set(world_space, device_space, camera, display, light, shading)
    window.show()


if __name__ == '__main__':
    main()

import copy
import datetime

from camera import Camera
from display import Display
from space import Space
from window import Window
import transform


def main():
    print('Reading ...')
    start = datetime.datetime.now()

    house_world = Space()
    house_world.append_by_file('house.d.txt')  # change geometry data

    camera = Camera()
    camera.set_by_file('camera.house.d.txt')  # change camera profile

    display = Display()
    display.set(800)  # change window size

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    print('Calculating #1 ...')
    start = datetime.datetime.now()

    house_view = copy.deepcopy(house_world)
    house_view.transform(transform.world_to_view, camera)

    house_screen = copy.deepcopy(house_view)
    house_screen.transform(transform.view_to_screen, camera)

    house_device = copy.deepcopy(house_screen)
    house_device.transform(transform.screen_to_device, display)

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    print('Calculating #2 ...')
    start = datetime.datetime.now()

    screen = Window()
    screen.set(house_device, display)

    cost = datetime.datetime.now() - start
    print('Finish. (cost = ' + str(cost) + ')\n')

    screen.show()


if __name__ == '__main__':
    main()
